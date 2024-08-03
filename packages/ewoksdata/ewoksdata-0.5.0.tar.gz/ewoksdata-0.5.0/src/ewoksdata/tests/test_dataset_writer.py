import time
import itertools

import h5py
import numpy
import pytest
from ..data.hdf5 import dataset_writer


@pytest.mark.parametrize("npoints", (1, 3, 1000))
@pytest.mark.parametrize("flush_period", (None, 0.1))
@pytest.mark.parametrize("known_npoints", (True, False))
def test_dataset_writer(tmpdir, npoints, flush_period, known_npoints):
    expected = list()
    filename = str(tmpdir / "test.h5")
    if flush_period is None:
        sleep_time = None
    else:
        sleep_time = flush_period + 0.1
    isleep = npoints // 3

    kwargs = {"flush_period": flush_period}
    if known_npoints:
        kwargs["npoints"] = npoints

    with h5py.File(filename, mode="w") as f:
        with dataset_writer.DatasetWriter(f, "data", **kwargs) as writer:
            for ipoint in range(npoints):
                data = numpy.random.random((10, 20))
                writer.add_point(data)
                expected.append(data)
                if sleep_time and ipoint == isleep:
                    time.sleep(sleep_time)

    with h5py.File(filename, mode="r") as f:
        data = f["data"][()]
    numpy.testing.assert_allclose(data, expected)


@pytest.mark.parametrize("nstack", (1, 4))
@pytest.mark.parametrize("npoints", (1, 3, 1000))
@pytest.mark.parametrize("flush_period", (None, 0.1))
@pytest.mark.parametrize("known_npoints", (True, False))
@pytest.mark.parametrize("known_nstack", (True, False))
@pytest.mark.parametrize("append_stacks_in_parallel", (True, False))
def test_stack_dataset_writer(
    tmpdir,
    nstack,
    npoints,
    flush_period,
    known_npoints,
    known_nstack,
    append_stacks_in_parallel,
):
    expected = [list() for _ in range(nstack)]
    filename = str(tmpdir / "test.h5")
    if flush_period is None:
        sleep_time = None
    else:
        sleep_time = flush_period + 0.1
    isleep = (nstack * npoints) // 3

    kwargs = {"flush_period": flush_period}
    if known_npoints:
        kwargs["npoints"] = npoints
    if known_nstack:
        kwargs["nstack"] = nstack

    if append_stacks_in_parallel:
        itpoints = itertools.product(range(npoints), range(nstack))
    else:
        itpoints = itertools.product(range(nstack), range(npoints))

    with h5py.File(filename, mode="w") as f:
        with dataset_writer.StackDatasetWriter(f, "data", **kwargs) as writer:
            for tpl in itpoints:
                if append_stacks_in_parallel:
                    ipoint, istack = tpl
                else:
                    istack, ipoint = tpl
                data = numpy.random.random((10, 20))
                writer.add_point(data, istack)
                expected[istack].append(data)
                if sleep_time and (ipoint * nstack + istack) == isleep:
                    time.sleep(sleep_time)

    with h5py.File(filename, mode="r") as f:
        data = f["data"][()]
    numpy.testing.assert_allclose(data, expected)
