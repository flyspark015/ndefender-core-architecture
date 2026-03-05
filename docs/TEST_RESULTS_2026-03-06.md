# Test Results 2026-03-06
- status_keys: PASS (ok)
- os_populated: PASS (ok)
- ups_populated: PASS (ok)
- esp32_status: PASS (ok)
- antsdr_status: PASS (ok)
- remoteid_status: PASS (ok)
- placeholders_status: PASS (ok)
- health_keys: PASS (ok)
- os_health: PASS (ok)
- ups_health: PASS (ok)
- esp32_health: PASS (ok)
- antsdr_health: PASS (ok)
- remoteid_health: PASS (ok)
- placeholders_health: PASS (ok)
- contacts_keys: PASS (ok)
- ws_hello: PASS (ok)

SUMMARY Total=16 PASS=16 FAIL=0 SKIP=0

# PHASE C.7 STEP 3 GATES
- `pytest -q`
```
............                                                          [100%]
=============================== warnings summary ===============================
app/main.py:23
  /home/toybook/ndefender-unified-backend/app/main.py:23: DeprecationWarning: 
          on_event is deprecated, use lifespan event handlers instead.
  
          Read more about it in the
          [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).
          
    @app.on_event("startup")

.venv/lib/python3.11/site-packages/fastapi/applications.py:4599
  /home/toybook/ndefender-unified-backend/.venv/lib/python3.11/site-packages/fastapi/applications.py:4599: DeprecationWarning: 
          on_event is deprecated, use lifespan event handlers instead.
  
          Read more about it in the
          [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).
          
    return self.router.on_event(event_type)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
15 passed, 2 warnings in 1.63s
```
- `python3 scripts/run_evidence.py`
```
SUMMARY Total=16 PASS=16 FAIL=0 SKIP=0
```
