// simple kdb for websocket gen
// running 32bit kdb 3.6

system "p 5001"
.z.ws:{show x;if[x~"grab";x:.j.j getlabels];neg[.z.w] x}
.z.wo:{show "hello - open connection";`activeWSConnections upsert (x;.z.t)}

getlabels:`labels`values!(("January";"February";"March";"April";"May";"June";"July";"August");(10 9 8 7 6 4 7 8))