from pydantic import BaseModel


class Record(BaseModel):
    """Class for holding a record from the SLURM Completed Logs file."""
    jobid: str
    userid: str
    groupid: str
    name: str
    jobstate: str
    partition: str
    timelimit: str
    starttime: str
    endtime: str
    nodelist: str
    nodecnt: str
    proccnt: str
    workdir: str
    reservationname: str
    gres: str
    account: str
    qos: str
    wckey: str
    cluster: str
    submittime: str
    eligibletime: str
    derivedexitcode: str
    exitcode: str
