from mindwm import logging
from mindwm.model.events import IoDocument
from mindwm.knfunc.decorators import iodoc, app

logger = logging.getLogger(__name__)

@iodoc
async def func(
        iodocument: IoDocument,
        graph, 
        uuid: str,
        username: str,
        hostname: str,
        socket_path: str,
        session_id: str,
        pane_title: str):

    user = graph.User(username=username).merge()
    host = graph.Host(hostname=hostname).merge()
    tmux = graph.Tmux(socket_path=socket_path).merge()
    sess = graph.TmuxSession(name=session_id).merge()
    pane = graph.TmuxPane(title=pane_title).merge()
    iodoc = graph.IoDocument(
            uuid=uuid,
            input=iodocument.input,
            output=iodocument.output,
            ps1=iodocument.ps1
        ).create()
    graph.UserHasHost(source=user, target=host).merge()
    graph.HostHasTmux(source=host, target=tmux).merge()
    graph.TmuxHasTmuxSession(source=tmux, target=sess).merge()
    graph.UserHasTmux(source=user, target=tmux).merge()
    graph.TmuxSessionHasTmuxPane(source=sess, target=pane).merge()
    graph.TmuxPaneHasIoDocument(source=pane, target=iodoc).merge()
    graph.IoDocumentHasUser(source=iodoc, target=user).merge()

    logger.info(iodoc)
