from app.security import ApprovalStore


def test_approval_is_bound_to_action_and_one_use():
    store = ApprovalStore(ttl_seconds=30)
    approval = store.request("delete_file")
    assert not store.consume(approval.token, "send_email")
    assert store.consume(approval.token, "delete_file")
    assert not store.consume(approval.token, "delete_file")


def test_unknown_token_is_rejected():
    store = ApprovalStore()
    assert not store.consume("not-a-token", "dangerous_action")
