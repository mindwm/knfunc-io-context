from mindwm import logging
from mindwm.model.events import IoDocument
from mindwm.knfunc.decorators import iodoc, app

logger = logging.getLogger(__name__)

@iodoc
async def io_context(
        iodocument: IoDocument,
        graph, 
        uuid: str,
        username: str,
        hostname: str,
        socket_path: str,
        session_id: str,
        pane_title: str):

    traceparent = iodocument.traceparent
    user = graph.User(username=username, traceparent=traceparent).merge()
    host = graph.Host(hostname=hostname, traceparent=traceparent).merge()
    tmux = graph.Tmux(socket_path=socket_path, traceparent=traceparent).merge()
    sess = graph.TmuxSession(name=session_id, traceparent=traceparent).merge()
    pane = graph.TmuxPane(title=pane_title, traceparent=traceparent).merge()
    iodoc = graph.IoDocument(
            uuid=uuid,
            input=iodocument.input,
            output=iodocument.output,
            ps1=iodocument.ps1,
            traceparent=iodocument.traceparent,
            tracestate=iodocument.tracestate
        ).create()
    graph.UserHasHost(source=user, target=host, traceparent=traceparent).merge()
    graph.HostHasTmux(source=host, target=tmux, traceparent=traceparent).merge()
    graph.TmuxHasTmuxSession(source=tmux, target=sess, traceparent=traceparent).merge()
    graph.UserHasTmux(source=user, target=tmux, traceparent=traceparent).merge()
    graph.TmuxSessionHasTmuxPane(source=sess, target=pane, traceparent=traceparent).merge()
    graph.TmuxPaneHasIoDocument(source=pane, target=iodoc, traceparent=traceparent).merge()
    graph.IoDocumentHasUser(source=iodoc, target=user, traceparent=traceparent).merge()

    logger.info(iodoc)
