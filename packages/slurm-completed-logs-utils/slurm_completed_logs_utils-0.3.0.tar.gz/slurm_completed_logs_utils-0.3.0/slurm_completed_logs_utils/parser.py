"""Class for parsing the SLURM Completed Logs text files."""
import logging
import os

from record import Record
import constants
from file_utils import check_infile_status


class Parser:
    """Class for parsing the SLURM Completed Logs files."""

    def __init__(self, **kwargs):
        """Constructor for Parser"""
        self.config = kwargs.get("config", None)
        self.config_file = kwargs.get("config_file", None)
        self.logfile = kwargs.get("logfile", None)
        self.outdir = kwargs.get("outdir", None)
        self.verbose = kwargs.get("verbose", constants.DEFAULT_VERBOSE)

        self.is_parsed = False
        self.rec_ctr = 0
        self.rec_list = []

        logging.info(f"Instantiated Parser in file '{os.path.abspath(__file__)}'")

    def get_records(self, infile: str) -> bool:
        """Parse the SLURM Completed Logs text file and retrieve a list of records.

        Args:
            infile (str): The SLURM Completed Logs text file to be parsed.
        Returns:
            List(Record): The parsed records.
        """
        if self.is_parsed:
            return self.rec_list

        check_infile_status(infile)

        # Sample record:
        # JobId=24226086 UserId=root(0) GroupId=root(0) Name=2419987.AGGAGGAA-GTGCTTAC_sample_internal_status_fail.sh JobState=CANCELLED Partition=PROD TimeLimit=UNLIMITED StartTime=2024-02-26T14:35:32 EndTime=2024-02-26T14:35:32 NodeList=(null) NodeCnt=0 ProcCnt=0 WorkDir=/root ReservationName= Gres= Account=root QOS=panels WcKey= Cluster=cluster SubmitTime=2024-02-24T16:05:19 EligibleTime=unknown DerivedExitCode=0:0 ExitCode=0:0

        with open(infile) as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 0:
                    continue
                record = Record(
                    jobid=parts[0].split('=')[1],
                    userid=parts[1].split('=')[1],
                    groupid=parts[2].split('=')[1],
                    name=parts[3].split('=')[1],
                    jobstate=parts[4].split('=')[1],
                    partition=parts[5].split('=')[1],
                    timelimit=parts[6].split('=')[1],
                    starttime=parts[7].split('=')[1],
                    endtime=parts[8].split('=')[1],
                    nodelist=parts[9].split('=')[1],
                    nodecnt=parts[10].split('=')[1],
                    proccnt=parts[11].split('=')[1],
                    workdir=parts[12].split('=')[1],
                    reservationname=parts[13].split('=')[1],
                    gres=parts[14].split('=')[1],
                    account=parts[15].split('=')[1],
                    qos=parts[16].split('=')[1],
                    wckey=parts[17].split('=')[1],
                    cluster=parts[18].split('=')[1],
                    submittime=parts[19].split('=')[1],
                    eligibletime=parts[20].split('=')[1],
                    derivedexitcode=parts[21].split('=')[1],
                    exitcode=parts[22].split('=')[1],
                )

                self.rec_list.append(record)
                self.rec_ctr += 1

        logging.info(f"Parsed '{self.rec_ctr}' records in SLURM Completed Logs file '{infile}'")

        self.is_parsed = True
        return self.rec_list
