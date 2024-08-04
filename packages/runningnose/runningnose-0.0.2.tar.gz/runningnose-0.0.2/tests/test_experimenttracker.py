from runningnose import ExperimentTracker


def test_experimenttracker():
    tracker = ExperimentTracker()
    assert isinstance(tracker, ExperimentTracker)
    assert tracker.experiment_name is None
    assert tracker.job_name is None


def test_experimenttracker_set():
    tracker = ExperimentTracker(root_dir="tests/sandbox")
    tracker.set_experiment()
    tracker.set_job()
    assert isinstance(tracker, ExperimentTracker)
    assert isinstance(tracker.experiment_name, str)
    assert isinstance(tracker.job_name, str)
    assert len(tracker.job_name) == 24


def test_experimenttracker_set_names():
    tracker = ExperimentTracker(root_dir="tests/sandbox")
    tracker.set_experiment("exp")
    tracker.set_job("job")
    assert isinstance(tracker, ExperimentTracker)
    assert isinstance(tracker.experiment_name, str)
    assert tracker.experiment_name == "exp"
    assert isinstance(tracker.job_name, str)
    assert tracker.job_name == "job"
