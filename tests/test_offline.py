"""Offline-Tests ohne OpenAI, Chroma oder weitere Test-Frameworks."""

import json
import unittest
from pathlib import Path

from training_rag.documents import load_chunks
from training_rag.metrics import calculate_metrics
from training_rag.pipeline import is_visible, load_users, reciprocal_rank_fusion


class SeminarLabOfflineTests(unittest.TestCase):
    def test_manifest_and_chunk_ids(self):
        chunks = load_chunks()
        self.assertEqual(len({item.document_id for item in chunks}), 16)
        ids = {item.chunk_id for item in chunks}
        mapping_file = (Path(__file__).resolve().parents[1]
                        / "data/evaluation/evidence_mapping.json")
        mapping = json.loads(mapping_file.read_text(encoding="utf-8"))
        for evidence in mapping.values():
            if evidence["status"] == "exact":
                self.assertTrue(set(evidence["chunks"]) <= ids)

    def test_acl(self):
        metadata = {chunk.document_id: chunk.metadata for chunk in load_chunks()}
        users = load_users()
        self.assertTrue(is_visible(metadata["D003"], users["anonymous"]))
        self.assertTrue(is_visible(metadata["D008"], users["customer_basic"]))
        self.assertFalse(is_visible(metadata["D008"], users["customer_cobalt"]))
        self.assertTrue(is_visible(metadata["D009"], users["teralune_engineer"]))
        self.assertFalse(is_visible(metadata["D010"], users["teralune_engineer"]))
        self.assertTrue(is_visible(metadata["D010"], users["security_admin"]))

    def test_metrics_and_rrf(self):
        result = calculate_metrics(["x", "a", "b"], {"a", "b"}, top_k=3)
        self.assertEqual(result["hit"], 1)
        self.assertAlmostEqual(result["precision"], 2 / 3)
        self.assertEqual(result["recall"], 1)
        self.assertEqual(result["mrr"], 0.5)
        fused = reciprocal_rank_fusion([
            [{"id": "a"}, {"id": "b"}],
            [{"id": "b"}, {"id": "a"}],
        ])
        self.assertEqual({cid for cid, _ in fused}, {"a", "b"})


if __name__ == "__main__":
    unittest.main()
