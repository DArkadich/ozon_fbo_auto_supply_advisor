from src import main


def test_job_runs_without_crash(monkeypatch):
    monkeypatch.setattr(main, "get_stocks", lambda: [{"product_id": 1}])
    monkeypatch.setattr(main, "get_recommendations", lambda: [{"product_id": 1}])
    monkeypatch.setattr(main, "prepare_report", lambda *a, **k: [])
    monkeypatch.setattr(main, "send_report", lambda *a, **k: None)
    monkeypatch.setattr(main, "upload_to_sheet", lambda *a, **k: None)
    main.job()  # не должно упасть
