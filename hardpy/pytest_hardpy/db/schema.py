# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from hardpy.pytest_hardpy.utils import TestStatus as Status


class IBaseResult(BaseModel):
    """Base class for all result models."""

    model_config = ConfigDict(extra="forbid")

    status: Status
    stop_time: int | None
    start_time: int | None
    name: str


class CaseStateStore(IBaseResult):
    """Test case description.

    Example:
    "test_one": {
        "status": "passed",
        "name": "Test 2",
        "start_time": 1695817188,
        "stop_time": 1695817189,
        "assertion_msg": null,
        "msg": null
    }
    """
    artifact: Optional[dict] = {}
    assertion_msg: str | None = None
    msg: dict | None = None


class CaseRunStore(IBaseResult):
    """Test case description with artifact.

    Example:
    "test_one": {
        "status": "passed",
        "name": "Test 2",
        "start_time": 1695817188,
        "stop_time": 1695817189,
        "assertion_msg": null,
        "msg": null,
        "artifact": {},
        "dependency": {}
    }
    """

    assertion_msg: str | None = None
    msg: dict | None = None
    artifact: Optional[dict] = {}
    dependency: Optional[dict] = {}


class ModuleStateStore(IBaseResult):
    """Test module description.

    Example:
    "test_2_b": {
      "status": "passed",
      "name": "Module 2",
      "start_time": 1695816886,
      "stop_time": 1695817016,
      "dependency": {},
      "cases": {
        "test_one": {
          "status": "passed",
          "name": "Test 1",
          "start_time": 1695817015,
          "stop_time": 1695817016,
          "assertion_msg": null,
          "msg": null
        }
      }
    }
    """
    dependency: Optional[dict] = {}
    cases: dict[str, CaseStateStore] = {}


class ModuleRunStore(IBaseResult):
    """Test module description.

    Example:
    "test_2_b": {
      "status": "passed",
      "name": "Module 2",
      "start_time": 1695816886,
      "stop_time": 1695817016,
      "artifact": {},
      "dependency": {},
      "cases": {
        "test_one": {
          "status": "passed",
          "name": "Test 1",
          "start_time": 1695817015,
          "stop_time": 1695817016,
          "assertion_msg": null,
          "msg": null,
          "artifact": {}
        }
      }
    }
    """
    dependency: Optional[dict] = {}
    cases: dict[str, CaseRunStore] = {}
    artifact: Optional[dict] = {}


class Dut(BaseModel):
    """Device under test description.

    Example:
    "dut": {
        "serial_number": "a9ad8dca-2c64-4df8-a358-c21e832a32e4",
        "info": {
        "batch": "test_batch",
        "board_rev": "rev_1"
        }
    },
    """

    model_config = ConfigDict(extra="forbid")

    serial_number: str | None
    info: dict = {}


class ResultStateStore(IBaseResult):
    """Test run description.

    Example:
    {
      "_rev": "44867-3888ae85c19c428cc46685845953b483",
      "_id": "current",
      "progress": 100,
      "stop_time": 1695817266,
      "timezone": [
        "CET",
        "CET"
      ],
      "start_time": 1695817263,
      "status": "failed",
      "name": "hardpy-stand",
      "dut": {
        "serial_number": "92c5a4bb-ecb0-42c5-89ac-e0caca0919fd",
        "info": {
          "batch": "test_batch",
          "board_rev": "rev_1"
        }
      },
      "test_stand": {
        "name": "Test stand 1"
      },
      "drivers": {
        "driver_1": "driver info",
        "driver_2": {
          "state": "active",
          "port": 8000
        }
      },
      "modules": {
        "test_1_a": {
          "status": "failed",
          "name": "Module 1",
          "start_time": 1695816884,
          "stop_time": 1695817265,
          "dependency": {},
          "cases": {
            "test_dut_info": {
              "status": "passed",
              "name": "DUT info ",
              "start_time": 1695817263,
              "stop_time": 1695817264,
              "assertion_msg": null,
              "msg": null,
              "dependency": {},
            },
            "test_minute_parity": {
              "status": "failed",
              "name": "Test 1",
              "start_time": 1695817264,
              "stop_time": 1695817264,
              "assertion_msg": "The test failed because minute 21 is odd! Try again!",
              "msg": [
                "Current minute 21"
              ],
              "dependency": {},
            },
          }
        },
      }
    }
    """

    model_config = ConfigDict(extra="forbid")

    rev: str = Field(..., alias="_rev")
    id: str = Field(..., alias="_id")
    progress: int
    timezone: tuple[str, str] | None = None
    test_stand: dict = {}
    dut: Dut
    modules: dict[str, ModuleStateStore] = {}
    drivers: Optional[dict] = {}


class ResultRunStore(IBaseResult):
    """Test run description.

    Example:
    {
      "_rev": "44867-3888ae85c19c428cc46685845953b483",
      "_id": "current",
      "progress": 100,
      "stop_time": 1695817266,
      "timezone": [
        "CET",
        "CET"
      ],
      "start_time": 1695817263,
      "status": "failed",
      "name": "hardpy-stand",
      "dut": {
        "serial_number": "92c5a4bb-ecb0-42c5-89ac-e0caca0919fd",
        "info": {
          "batch": "test_batch",
          "board_rev": "rev_1"
        }
      },
      "test_stand": {
        "name": "Test stand 1"
      },
      "drivers": {
        "driver_1": "driver info",
        "driver_2": {
          "state": "active",
          "port": 8000
        }
      },
      "artifact": {},
      "modules": {
        "test_1_a": {
          "status": "failed",
          "name": "Module 1",
          "start_time": 1695816884,
          "stop_time": 1695817265,
          "artifact": {},
          "dependency": {},
          "cases": {
            "test_dut_info": {
              "status": "passed",
              "name": "DUT info",
              "start_time": 1695817263,
              "stop_time": 1695817264,
              "assertion_msg": null,
              "msg": null,
              "artifact": {},
              "dependency": {},
            },
            "test_minute_parity": {
              "status": "failed",
              "name": "Test 1",
              "start_time": 1695817264,
              "stop_time": 1695817264,
              "assertion_msg": "The test failed because minute 21 is odd! Try again!",
              "msg": [
                "Current minute 21"
              ],
              "dependency": {},
              "artifact": {
                "data_str": "123DATA",
                "data_int": 12345,
                "data_dict": {
                  "test_key": "456DATA"
                }
              }
            },
          }
        },
      }
    }
    """

    model_config = ConfigDict(extra="forbid")

    rev: str = Field(..., alias="_rev")
    id: str = Field(..., alias="_id")
    progress: int
    timezone: tuple[str, str] | None = None
    test_stand: dict = {}
    dut: Dut
    modules: dict[str, ModuleRunStore] = {}
    drivers: Optional[dict] = {}
    artifact: Optional[dict] = {}
