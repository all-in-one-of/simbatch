from simbatch.core import core
from simbatch.core import io as inout
from simbatch.core import common
import pytest

# TODO check dir on prepare tests
TESTING_AREA_DIR = "S:\\simbatch\\data\\"

@pytest.fixture(scope="module")
def io():
    sib = core.SimBatch(5, ini_file="S:/simbatch/simbatch/config.ini")
    sib.clear_all_memory_data()
    sib.p.create_example_project_data(do_save=False)
    sib.p.update_current_from_index(1)
    return inout.InOutStorage(sib)


def test_get_flat_name(io):
    assert io.get_flat_name("abc") == "abc"
    assert io.get_flat_name("ab c") == "ab_c"
    assert io.get_flat_name("a b c") == "a_b_c"


def test_loaded_sample_project(io):
    assert io.batch.p.total_projects == 3
    assert io.batch.p.projects_data[1].project_name == "Sample Project 2"


def test_generate_base_setup_file_name(io):
    tuple_base_setup = io.generate_tuple_base_setup_file_name(schema_name="test_schema")
    assert  tuple_base_setup[0] == 1
    assert  tuple_base_setup[1] == "D:\\proj\\fx\\test_schema\\base_setup\\test_schema_v001.null"





