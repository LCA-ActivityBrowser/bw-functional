"""bw2data 4.7 vs 4.8 project_changed receiver compatibility."""


class _FakeProjectDataset:
    name = "compat-test"
    data = {"bw_functional_version": "already-current"}

    def save(self):
        raise AssertionError("save should not run when version is already current")


def test_check_and_update_accepts_bw2data_47_positional_sender(monkeypatch):
    import bw_functional as bf

    monkeypatch.setattr(bf, "latest", "already-current")
    ds = _FakeProjectDataset()
    # bw2data ≤4.7: project_changed.send(dataset)
    bf._check_and_update(ds)


def test_check_and_update_accepts_bw2data_48_dataset_kwarg(monkeypatch):
    import bw_functional as bf

    monkeypatch.setattr(bf, "latest", "already-current")
    ds = _FakeProjectDataset()
    # bw2data 4.8+: project_changed.send(manager, dataset=dataset)
    bf._check_and_update(object(), dataset=ds)
