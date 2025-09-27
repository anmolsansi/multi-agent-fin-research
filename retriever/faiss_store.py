# retriever/faiss_store.py
import json
import pathlib
import numpy as np

try:
    import faiss  ## Not available for apple silicon

    HAVE_FAISS = True
except Exception:
    HAVE_FAISS = False


class FaissStore:
    def __init__(self, dim=384, dirpath="indices"):
        self.dim = dim
        self.dir = pathlib.Path(dirpath);
        self.dir.mkdir(parents=True, exist_ok=True)
        self.idx_path = self.dir / "faiss.index"
        self.meta_path = self.dir / "meta.jsonl"
        self.meta = []

        if HAVE_FAISS and self.idx_path.exists():
            self.index = faiss.read_index(str(self.idx_path))
        elif HAVE_FAISS:
            self.index = faiss.IndexFlatIP(dim)
        else:
            # fallback: store vectors in memory as numpy array
            self.index = None
            self._vecs = None

        if self.meta_path.exists():
            with open(self.meta_path, "r", encoding="utf-8") as f:
                self.meta = [json.loads(l) for l in f]

    def add(self, vectors, metadatas):
        vec = np.array(vectors, dtype="float32")
        if HAVE_FAISS:
            self.index.add(vec)
        else:
            self._vecs = vec if self._vecs is None else np.vstack([self._vecs, vec])
        self.meta.extend(metadatas)

    def persist(self):
        if HAVE_FAISS:
            faiss.write_index(self.index, str(self.idx_path))
        with open(self.meta_path, "w", encoding="utf-8") as f:
            for m in self.meta:
                f.write(json.dumps(m, ensure_ascii=False) + "\n")

    def search(self, query_vec, k=8):
        q = np.array([query_vec], dtype="float32")
        if HAVE_FAISS:
            D, I = self.index.search(q, k)
            out = []
            for j, i in enumerate(I[0]):
                if i == -1: continue
                out.append((self.meta[i], float(D[0][j])))
            return out
        else:
            # cosine with normalized embeddings (dot product)
            sims = (self._vecs @ q[0])
            idxs = np.argsort(-sims)[:k]
            return [(self.meta[int(i)], float(sims[int(i)])) for i in idxs]
