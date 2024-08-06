import datetime
import os
from struct import calcsize, iter_unpack, unpack

import numpy as np
import xarray as xr
import logging

# set up the logger and set the logging level
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# generate a handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


def decode_nusdas(fname):
    n = os.path.getsize(fname)
    print("file size=", n)
    logger.info(f"decode_nusdas: filesize={n} bytes")

    mdls = []
    surfs = []
    outs, dtims, levels, elements = [], [], [], []
    dtim_base = datetime.datetime(1801, 1, 1, 0, 0)  # base datetime counted by minutes

    with open(fname, mode="rb") as f:
        while True:  # loop over records
            head_pos = f.tell()
            (record_length,) = unpack(">I", f.read(4))
            c_header = f.read(4).decode("utf-8")
            (_,) = unpack(">I", f.read(4))
            (time,) = unpack(">I", f.read(4))
            create_time = datetime.datetime.fromtimestamp(time, datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            logger.debug(f"{c_header}, {record_length}, {create_time}")

            if c_header == "NUSD":
                prod = f.read(72).decode("utf-8")
                _ = f.read(8)
                (nus_version,) = unpack(">I", f.read(4))
                (filesize,) = unpack(">I", f.read(4))
                (nrecords,) = unpack(">I", f.read(4))
                logger.info(f"{prod}, {nus_version}, {filesize}, {nrecords}")

            if c_header == "CNTL":
                #
                typ = f.read(16).decode("utf-8")
                iymdh = f.read(12).decode("utf-8")  # initial time
                (initm,) = unpack(">I", f.read(4))  # initial time in total mins from 1801.1.1
                tunit = f.read(4).decode("utf-8")  # minutes
                (nmem,) = unpack(">I", f.read(4))
                (nft,) = unpack(">I", f.read(4))
                (nlev,) = unpack(">I", f.read(4))
                (nvar,) = unpack(">I", f.read(4))
                proj = f.read(4).decode("utf-8")
                # jump to interesting records
                f.seek(head_pos + 172, 0)
                (_,) = unpack(">I", f.read(4))
                (validm,) = unpack(">I", f.read(4))
                vymdh = (dtim_base + datetime.timedelta(minutes=validm)).strftime("%Y%m%d%H%M")
                (_,) = unpack(">I", f.read(4))
                (_,) = unpack(">I", f.read(4))

                ftm = validm - initm
                logger.info(f"init: {iymdh}, valid:{vymdh}, ft:{ftm}")

            if c_header == "INDX":
                """For NuSDaS < 1.3"""
                ...
            if c_header == "INDY":
                """For NuSDaS >= 1.3"""
                ...
            if c_header == "SUBC":
                ...
            if c_header == "INFO":
                ...

            if c_header == "DATA":
                _ = f.read(4).decode("utf-8")
                # f.seek(20 - 8, 1)
                (nt1,) = unpack(">I", f.read(4)) # load valid time
                (nt2,) = unpack(">I", f.read(4)) 

                logger.debug(f"DATA valid time: {dtim_base + datetime.timedelta(minutes=nt1)}")

                c_level = f.read(12).decode()[:6]  # lebel name
                c_element = f.read(6).decode().strip()  # element name
                if c_element not in ["RU", "RV", "RW", "QV", "DNSG2", "PSEA", "PRS", "SMQR"]:
                    f.seek(head_pos + record_length + 8, 0)
                    continue

                dtims.append(dtim_base + datetime.timedelta(minutes=nt1))
                levels.append(c_level)
                elements.append(c_element)

                f.seek(2, 1)  # skip the reserved blank
                (nx,) = unpack(">I", f.read(4))
                (ny,) = unpack(">I", f.read(4))

                # currently only unpacking 2UPC
                # TODO: implement other packing methods
                c_packing = f.read(4).decode()
                c_missing = f.read(4).decode()
                base = unpack(">f", f.read(4))[0]
                ampl = unpack(">f", f.read(4))[0]
                pack = np.array([i[0] for i in iter_unpack(">H".format(nx * ny), f.read(nx * ny * 2))]).reshape(ny, nx)
                values = base + ampl * pack

                if c_level == "SURF  ":
                    surfs.append(
                        xr.DataArray(
                            data=values[::-1, :, np.newaxis, np.newaxis],
                            dims=["y", "x", "level", "time"],
                            coords=dict(
                                time=[dtim_base + datetime.timedelta(minutes=nt1)],
                                level=["SURF"],
                                # reference_time=reference_time,
                            ),
                            attrs=dict(
                                description="Ambient temperature.",
                                units="degC",
                            ),
                        )
                        .rename(c_element)
                    )
                else:
                    mdls.append(
                        xr.DataArray(
                            data=values[::-1, :, np.newaxis, np.newaxis],
                            dims=["y", "x", "level", "time"],
                            coords=dict(
                                time=[dtim_base + datetime.timedelta(minutes=nt1)],
                                level=[int(c_level)],
                                # reference_time=reference_time,
                            ),
                            attrs=dict(
                                description="Ambient temperature.",
                                units="degC",
                            ),
                        )
                        .rename(c_element)
                    )

            elif c_header == "END ":
                break
            f.seek(head_pos + record_length + 8, 0)

    return xr.merge(mdls), xr.merge(surfs)
