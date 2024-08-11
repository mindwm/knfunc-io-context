from mindwm import logging
from mindwm.model.events import IoDocument
import mindwm.model.graph as g
from mindwm.knfunc.decorators import iodocument_with_source, app

logger = logging.getLogger(__name__)

@iodocument_with_source
def func(
        iodocument: IoDocument,
        uuid: str,
        username: str,
        hostname: str,
        socket_path: str,
        tmux_session: str,
        tmux_pane: str):

    user = g.User(username=username).merge()
    host = g.Host(hostname=hostname).merge()

    socket_path = socket_path.strip("b'").strip('/')
    socket_path = f"{username}@{hostname}/{socket_path}"
    tmux = g.Tmux(socket_path=socket_path).merge()

    session_id = f"{socket_path}:{tmux_session}"
    sess = g.TmuxSession(name=session_id).merge()

    tmux_pane = f"{session_id}%{tmux_pane}"
    pane = g.TmuxPane(title=tmux_pane).merge()

    iodoc = g.IoDocument(
            uuid=uuid,
            input=iodocument.input,
            output=iodocument.output,
            ps1=iodocument.ps1
        ).create()
    g.UserHasHost(source=user, target=host).merge()
    g.HostHasTmux(source=host, target=tmux).merge()
    g.TmuxHasTmuxSession(source=tmux, target=sess).merge()
    g.UserHasTmux(source=user, target=tmux).merge()
    g.TmuxSessionHasTmuxPane(source=sess, target=pane).merge()
    g.TmuxPaneHasIoDocument(source=pane, target=iodoc).merge()
    g.IoDocumentHasUser(source=iodoc, target=user).merge()

    logger.info(iodoc)
