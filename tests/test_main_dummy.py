import src.main as main


def test_main_job_runs(monkeypatch):
    monkeypatch.setattr(main, "get_stocks", lambda: [])
    monkeypatch.setattr(main, "get_recommendations", lambda: [])
    monkeypatch.setattr(main, "prepare_report", lambda x, y: [])
    monkeypatch.setattr(main, "upload_to_sheet", lambda x: None)
    monkeypatch.setattr(main, "send_report", lambda x: None)
    main.job()
