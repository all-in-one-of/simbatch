import sys
import core.core as simbatch_core
import server.server as simbatch_server


no_gui_batch = simbatch_core.SimBatch("Server", ini_file="config.ini")

ret = no_gui_batch.load_data()
if ret[0] is not False and ret[0]>=0:
    server = simbatch_server.SimBatchServer(no_gui_batch)
    server.run(argv=sys.argv)
else:
    no_gui_batch.logger.err("Database NOT loaded properly !")
    

