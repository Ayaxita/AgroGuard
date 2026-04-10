declare module "thought-response" {
  interface ThoughtProcedure {
    debugging: {
      content: string;
    };
    elapsed: number;
    icon: string;
    index: number;
    name: string;
    node_name: string;
    plugin_type: number;
    reply_index: number;
    status: string;
    switch: string;
    title: string;
    workflow_name: string;
  }

  interface ThoughtPayload {
    elapsed: number;
    is_workflow: boolean;
    procedures: ThoughtProcedure[];
    record_id: string;
    request_id: string;
    session_id: string;
    trace_id: string;
    workflow_name: string;
  }

  interface ThoughtData {
    type: "thought";
    payload: ThoughtPayload;
    message_id: string;
  }

  type ThoughtResponse = ["thought", ThoughtData];
}
