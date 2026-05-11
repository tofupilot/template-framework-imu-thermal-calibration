def connect_dut(dut, log):
    log.info("Connecting to DUT...")
    dut.connect()
    log.info("DUT connected")
