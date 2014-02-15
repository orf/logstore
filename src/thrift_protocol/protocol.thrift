
struct LogLine {
    1: string file_name,
    2: string read_time,
    3: string log_line,
}

/* This service is called by the Daemon */
service ConductorService {
    bool got_log_line(1:LogLine line),
    bool got_log_lines(1:list<LogLine> lines),
    bool hello_world() // Used to test the connection
}

/* This internal service is only accessed by the web interface and the analyser */
service InternalConductorService {
    // Notifies the conductor of a percolator(s) hit
    oneway void percolator_hit(1:string logline, 2:string time, 3:string server_name, 4:string file_name, 5:set<string> hits)
}