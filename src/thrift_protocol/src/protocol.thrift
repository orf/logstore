
struct Event {
    1: i32 id,
    2: string name,
    3: string query
}


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
    // Terminate all connections from this server
    bool remove_server(1:i32 server_id),
    // Notifies the conductor when a new Event has been added
    bool create_event(1:Event event),
    // Notifies the conductor when an Event has been removed
    bool remove_event(1:i32 id),
    // Notifies the conductor of a percolator(s) hit
    oneway void percolator_hit(1:string logline, 2:string time, 3:i32 server_id,
                               4:string file_name, 5:set<string> hits, 6:string search_id)
}