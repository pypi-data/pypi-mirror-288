import numpy as np
import pytest

num_cells = 31
num_trains = 50


@pytest.fixture(scope="session")
def geom():
    from extra_redu.spi.tests.mock.agipd import AGIPDGeometry

    return AGIPDGeometry(downsample=8)


@pytest.fixture(scope="session")
def mask(geom):
    np.random.seed(seed=2)
    mask = geom.random_mask(num_cells, num_trains)
    return mask


@pytest.fixture(scope="session")
def spi_data(geom):
    from extra_redu.spi.tests.mock.models import spi_ball_scattering

    num_pulses = num_trains * num_cells
    model_param = dict(
        photon_en=6.0,  # keV
        L=1.7,  # m
        R=35,  # nm
        flow_size=12,  # um
        beam_size=1.5,  # um
        pulse_energy=1.8,  # mJ
        pulse_energy_rmsd=0.010,  # mJ
        # gas parameters
        gas_ambient=0.02,
        gas_shape=4e-5,
    )

    np.random.seed(seed=1)
    adu = spi_ball_scattering(geom, num_pulses, **model_param)
    return adu


@pytest.fixture(scope="session")
def spi_run(geom, mask, spi_data):
    from extra_redu.fileutils.tests.mock.extra_data import (
        MockDataCollection, MockSourceData)

    train_ids = list(range(10001, 10001 + num_trains))
    detector_id = "SPB_DET_AGIPD1M-1"
    source_names = [f"{detector_id}/CORR/{modno}CH0:output"
                    for modno in range(16)]

    cellId = np.tile(
        np.arange(num_cells, dtype=np.int32) + 1, num_trains)[:, None]
    pulseId = cellId.astype(np.uint64) * 4
    trainId = np.repeat(
        np.array(train_ids, dtype=np.uint64), num_cells)[:, None]
    count = np.full(num_trains, num_cells)
    data = {}
    for modno, source_id in enumerate(source_names):
        module_data = {
            "image.data": spi_data[:, modno],
            "image.mask": mask[:, modno],
            "image.cellId": cellId,
            "image.pulseId": pulseId,
            "image.trainId": trainId,
        }
        data[source_id] = MockSourceData(
            source_id, train_ids, count, module_data)

    return MockDataCollection.mock(train_ids, data=data)


@pytest.fixture(scope="session")
def litpx_counter(spi_run):
    from extra_redu.fileutils import StackedPulseSource
    from extra_redu.spi import LitPixelCounter

    detector_id = "SPB_DET_AGIPD1M-1"
    sources_ptrn = detector_id + r"/CORR/(?P<key>\d+)CH0:output"
    src = StackedPulseSource.from_datacollection(
        spi_run, sources_ptrn, "image")

    litpx_counter = LitPixelCounter(src)
    litpx_counter(src)

    return litpx_counter


@pytest.fixture()
def spi_ref():
    hit_ix = np.array([
          53,  101,  125,  154,  188,  240,  257,  427,  430,  451,  505,  # noqa: E131, E501
         535,  564,  722,  742,  754,  807,  810,  929,  944, 1000, 1013,  # noqa: E131, E501
        1116, 1121, 1130, 1209, 1316, 1343, 1384, 1443, 1476, 1477, 1496,  # noqa: E131, E501
        1497, 1503, 1523  # noqa: E131, E501
    ])
    miss_ix = np.array([
         180,  263,  265,  344,  386,  405,  420,  490,  518,  530,  618,  # noqa: E131, E501
         635,  654,  672,  675,  805,  848,  852,  876,  890,  893,  936,  # noqa: E131, E501
         972,  988, 1038, 1039, 1043, 1168, 1201, 1221, 1299, 1368, 1388,  # noqa: E131, E501
        1478, 1479, 1534  # noqa: E131, E501
    ])
    data_ix = np.sort(np.concatenate([hit_ix, miss_ix]))

    data_hitscore = np.array([
        96579,  85196,  33465, 100824,  18289,  34952,  63276,  55453,  # noqa: E131, E501
        10922,      0,  16732,      0,  11650,  17096,  75883,  63550,  # noqa: E131, E501
        56987,      0,  95783,      0,      0,  72089,  54867,      0,  # noqa: E131, E501
            0,   5577,      0,      0,  35288,  29789,  56987,   6721,  # noqa: E131, E501
        72507,  80099,  23831,  10922,      0,  20695,  24385,  60494,  # noqa: E131, E501
        18289,  49932,  17873,      0,  58982,  74898,   5461,   6096,  # noqa: E131, E501
         6721,  43690,  55606,  49932,  14979,  45197,  43690,      0,  # noqa: E131, E501
            0,  81139,  45590,   7281,  60494,  20695,  85481, 102300,  # noqa: E131, E501
        60494,  22469,   6898,  91750,  50412,  49152,  80099,   5461   # noqa: E131, E501
    ])
    return type("SpiHitfinderReference", (), dict(
        hit_ix=hit_ix, miss_ix=miss_ix, data_ix=data_ix,
        data_hitscore=data_hitscore,
    ))


@pytest.fixture()
def spi_adaptive_threshold():
    threshold = np.array([
        44637.61724588, 44637.61724588, 45835.57715573, 47590.0887202,
        33156.00616771, 30249.03908196, 30045.63527458, 30045.63527458,
        30308.62744633, 45763.4963824,  30567.67832997, 29117.79676195,
        30308.05966078, 42393.29510141, 41647.92159886, 42089.2649745,
        39809.73111137, 42873.29510141, 42257.2649745,  42257.2649745,
        41853.2649745,  41723.92159886, 25842.05705136, 29386.89295457,
        31194.73662673, 32834.76847349, 34756.45652947, 37661.19967975,
        54006.88388092, 47721.01702052, 47548.51702052, 47384.51702052,
        43256.18206618, 43652.18206618, 43736.18206618, 31812.00782825,
        27921.54513106, 33710.68093939, 46677.24386194, 40837.57869766,
        40078.47538845, 42320.79510141, 44706.83703001, 30877.95492824,
        40906.8705373,  37723.50177915, 31272.33281936, 29963.62744633,
        38155.90475626, 46928.38660894
    ])
    return threshold
