from typing import Callable
from EventHandler_Edog0049a import EventHandler 
from Twitch_Edog0049a.ChatInterface.MessageHandler import *
from IrcConnector_Edog0049a.IrcConnector import IrcConnector
import logging
@dataclass
class TCISettings:
    server: str = "irc.chat.twitch.tv"
    port: int = 6667
    user: str = None
    password: str = None
    channels: list = None
    caprequest: str = "twitch.tv/tags twitch.tv/commands twitch.tv/membership"
    SSL: bool = False

class TCI:
    """    
        Bulids connection, receives chat messages from server and emits corrisponding events! 

        This library closely follows twitch docs https://dev.twitch.tv/docs/irc

        All functions or methods used as event callbacks need to have 2 input varibles
         
        Example of how to use this

        .. literalinclude:: example.py

        This is the message object that is sent with event 

        .. _Message:

        .. code-block::
        
            class Message:
                raw: str # the raw unparsed message string from server
                channel: str # the channel the message is from  
                id: str # id of message 
                prefix: str # there is 3 types of prfixes 
                command: str # the is the command which is also the event name
                text: str # the context of the message 
                username: str # the person who has sent the message
                params: List[str] # this is a break down of the end of message 
                tags: Dict # these are twitch tags look 
        
        .. code-block::
        
            class Channel:
                name: str 
                roomID: str   
                mods: list 
                roomState: RoomState = RoomState()
                userState: UserState = UserState()
            
            class RoomState:
                emote_only: int 
                rituals: int 
                followers_only: int 
                r9k: int 
                slow: int  
                subs_only: int 

            class UserState:
                badge_info: str
                badges: dict 
                color: str 
                display_name: str
                emote_sets: str
                turbo: str
                user_id: str
                user_type: str
    """
    _COMMANDS: COMMANDS = COMMANDS()
    def __init__(self, settings=TCISettings()):
        self._settings: TCISettings = settings   
        self._messageHandler: MessageHandler = MessageHandler()
        self._event: EventHandler = EventHandler()
        self._globalUserState: globalUserState = globalUserState()
        self._channels: dict[str, Channel] = {} 
        # Register System Event functions
        self._event.on(self._COMMANDS.NOTICE, self._onNotice)
        self._event.on(self._COMMANDS.ROOMSTATE, self._onRoomState)
        self._event.on(self._COMMANDS.USERSTATE, self._setUserState)
        self._event.on(self._COMMANDS.MESSAGEIDS.ROOM_MODS, self._setChannelMods)
        self._event.on(self._COMMANDS.GLOBALUSERSTATE, self._setGlobalUserSate)
        self._event.on(self._COMMANDS.ROOMSTATE.EMOTE_ONLY, self._onEmotesOnly)
        self._event.on(self._COMMANDS.ROOMSTATE.FOLLOWERS_ONLY, self._onFollowersOnly)
        self._event.on(self._COMMANDS.ROOMSTATE.SLOW, self._onSlowMode)
        self._event.on(self._COMMANDS.ROOMSTATE.SUBS_ONLY, self._onSubsOnly)
        self._event.on(self._COMMANDS.ROOMSTATE.R9K, self._onR9k)
        self._event.on(self._COMMANDS.LOGIN_UNSUCCESSFUL, self._onInvalidLogin)

    ########################################## IRC CONNECTOR SETUP ########################################################
    def _getIrcConnector(self):
        if self._settings.server and self._settings.port:
            self._IrcClient = IrcConnector(self._settings.server, self._settings.port, SSL=self._settings.SSL or False)
            self._IrcClient.on(self._IrcClient.EVENTS.MESSAGE, self._onIrcMessage)
            self._IrcClient.on(self._IrcClient.EVENTS.CONNECTED, self._onIrcConnect)
            self._IrcClient.on(self._IrcClient.EVENTS.DISCONNECT, self._onIrcDisconnect)
            self._IrcClient.on(self._IrcClient.EVENTS.ERROR, self._onIrcError)
        else: 
            self._IrcClient = None

    def _onIrcMessage(self, sender: IrcConnector, data: str):
        messageParts: List[str] = data.split("\r\n")
        for messagePart in messageParts:
            self._event.emit(self,self._COMMANDS.RECEIVED, messagePart)
            event, msg = self._messageHandler.handleMessage(messagePart)
            if event is not None:
                self._event.emit(self, event, msg)
    
    def _onIrcConnect( self, sender: IrcConnector, data):
        self._event.emit(self._COMMANDS.CONNECTED,"")
        if self._settings.channels is not None:
            self.join(self._settings.channels) 
            
    def _onIrcDisconnect(self,sender: IrcConnector, data):
        self._event.emit(self, self._COMMANDS.DISCONNECTED, "")    
           
    def _onIrcError(self,sender: IrcConnector, data):
        pass     
    #########################################################################################################################    
    def updateSettings(self, settings: TCISettings)->None:
        self._settings = settings
        self._IrcClient = self._getIrcConnector()
    
    def connect(self)->None:
        self._IrcClient.connect()

    def disconnect(self):
        if self.isConnected:
          self._IrcClient.disconnect()
    
    def send(self, data):
        self._IrcClient.send(data)

    @property
    def event(self) -> EventHandler:
        return self._event
    
    @property
    def isConnected(self) -> bool:
        return self._IrcClient.isConnected()

    @property
    def globalUserState(self) -> globalUserState:
        return self._globalUserState
    
    @property
    def channels(self) -> Dict[str, Channel]:
        return self._channels    
      
    def _login(self)->None:
        """[summary]
        """
        self.send(f"CAP REQ :{self._caprequest}")
        self.send(f"PASS {self._password}")          
        self.send(f"NICK {self._settings.user}")

    def _onInvalidLogin(self, sender: object, message)->None:
        self.disconnect()
        print(f"LOGIN FAIL!: {message}")
        

    def _onRoomState(self, sender: object, message)->None:
        """
        _onRoomState [summary]
        
        :param sender: what is reasponsible for event
        :type sender: object
        :param message: irc message
        :type message: Message
        """
        if len(message.tags) >= 3:
            self._setRoomState(message)
        elif len(message.tags) <= 2:
            self._updateRoomState(message)
                    
    def _onNotice(self, sender: object, message)->None:
        """
        _onNotice [summary]
        .
        :param sender: what is reasponsible for event
        :type sender: object
        :param message: irc message
        :type message: Message
        """
        self._event.emit(self, message.msgId, message) 

    def _setRoomState(self, message)->None:
        """
        _setRoomState [summary]
        
        :param channel: [description]
        :type channel: str
        :param tags: [description]
        :type tags: list
        """
        if message.channel not in self._channels:
            self._channels[message.channel] = MessageHandler.Channel()

        self._channels[message.channel].roomID = message.tags.get(self._COMMANDS.ROOMSTATE.ROOM_ID)
        self._channels[message.channel].name = message.channel

        for key in message.tags:
            if key != self._COMMANDS.ROOMSTATE.ROOM_ID:
                setattr(self._channels[message.channel].roomState, key.replace('-','_'), message.tags.get(key))
        self._getMods(message.channel)

    def _updateRoomState(self, message)->None:
        """
        _updateRoomState [summary]
        
        :param channel: [description]
        :type channel: str
        :param tags: [description]
        :type tags: dict
        """
        for key in message.tags:
            if key != self._COMMANDS.ROOMSTATE.ROOM_ID:
                setattr(self._channels[message.channel].roomState, key.replace('-','_'), message.tags.get(key))
                self._event.emit(self, key, message)

    def _setChannelMods(self, sender: object, message)->None:
        """
        _setChannelMods [summary]
        
        :param sender: [description]
        :type sender: object
        :param message: [description]
        :type message: Message
        """
        self._channels[message.channel].mods = message.params[1].split(':')[1].split(',')
    
    def _setUserState(self, sender, message):
        """[summary]
        
        :param sender: [description]
        :type sender: [type]
        :param message: [description]
        :type message: [type]
        """
        if message.channel not in self._channels:
            self._channels[message.channel] = MessageHandler.Channel()
        for key in message.tags:
            setattr(self._channels[message.channel].userState, key.replace('-','_'), message.tags.get(key))
        if self._channels[message.channel].userState.mod:
            self._channels[message.channel].tokenBucket.maxToken = 100 
        
    def _setGlobalUserSate(self, sender, message)->None:
        """[summary]
        
        :param sender: [description]
        :type sender: [type]
        :param message: [description]
        :type message: [type]
        """
        for key in message.tags:
            setattr(self._globalUserState, key.replace('-','_'), message.tags.get(key))
        
    def _getMods(self, channel: str)->None:
        """
        NO LONGR WORKS
        getMods [summary]
        
        :param channel: [description]
        :type channel: str
        """
        return
    
    def _onEmotesOnly(self, sender, message):
        """[summary]
        
        :param sender: [description]
        :type sender: [type]
        :param message: [description]
        :type message: [type]
        """
        if message.tags[self._COMMANDS.ROOMSTATE.EMOTE_ONLY]:
            self._event.emit(self, self._COMMANDS.ROOMSTATE.EMOTE_ONLY_ON, self._channels[message.channel])
        else:
            self._event.emit(self, self._COMMANDS.ROOMSTATE.EMOTE_ONLY_OFF, self._channels[message.channel])

    def _onFollowersOnly(self, sender, message):
        """[summary]
        
        :param sender: [description]
        :type sender: [type]
        :param message: [description]
        :type message: [type]
        """
        if int(message.tags[self._COMMANDS.ROOMSTATE.FOLLOWERS_ONLY] )> -1:
            self._event.emit(self, self._COMMANDS.ROOMSTATE.FOLLOWERS_ONLY_ON, self._channels[message.channel])
        else:
            self._event.emit(self, self._COMMANDS.ROOMSTATE.FOLLOWERS_ONLY_OFF, self._channels[message.channel])

    def _onSlowMode(self, sender, message):
        """[summary]
        
        :param sender: [description]
        :type sender: [type]
        :param message: [description]
        :type message: [type]
        """
        if int(message.tags[self._COMMANDS.ROOMSTATE.SLOW]) > 0:
            self._event.emit(self, self._COMMANDS.ROOMSTATE.SLOW_ON, self._channels[message.channel])
        else:
            self._event.emit(self, self._COMMANDS.ROOMSTATE.SLOW_OFF, self._channels[message.channel])

    def _onSubsOnly(self, sender, message):
        """[summary]
        
        :param sender: [description]
        :type sender: [type]
        :param message: [description]
        :type message: [type]
        """
        if message.tags[self._COMMANDS.ROOMSTATE.SUBS_ONLY]:
            self._event.emit(self, self._COMMANDS.ROOMSTATE.SUBS_ONLY_ON, self._channels[message.channel])
        else:
            self._event.emit(self, self._COMMANDS.ROOMSTATE.SUBS_ONLY_OFF, self._channels[message.channel])

    def _onR9k(self, sender, message):
        """[summary]
        
        :param sender: [description]
        :type sender: [type]
        :param message: [description]
        :type message: [type]
        """
        if message.tags[self._COMMANDS.ROOMSTATE.R9K]:
            self._event.emit(self, self._COMMANDS.ROOMSTATE.R9K_ON, self._channels[message.channel])
        else:
            self._event.emit(self, self._COMMANDS.ROOMSTATE.R9K_OFF, self._channels[message.channel])
    
    def _addChannel(self, channel: str)->None:
        """[summary]
        
        :param channel: [description]
        :type channel: str
        """
        if channel not in self._channels:
            channel = self._formatChannelName(channel)
            self._channels[channel] =  Channel()
            self._channels[channel].name = channel

    def _removeChannel(self, channel: str)->None:
        """[summary]
        
        :param channel: [description]
        :type channel: str
        """
        if channel in self._channels:
            channel = self._formatChannelName(channel)
            del(self._channels[channel])
    
    def _formatChannelName(self, channel:str)->str:
        """[summary]
        
        :param channel: [description]
        :type channel: str
        :return: [description]
        :rtype: str
        """
        return channel if channel.startswith("#") else f"#{channel}"

    def join(self, channels: list)->None:
        """
        join - jions channels
        
        :param channels: list of channel names
        :type channels: list[str]
        """
        for channel in channels:
            channel = self._formatChannelName(channel)
            self._addChannel(channel)
            self.send(f"JOIN {channel}")
    
    def part(self, channels: list):
        """ 
        part - Leaves channel
        
        :param channels: list of channel names
        :type channels: list[str]
        """
        for channel in channels:
            channel = self._formatChannelName(channel)
            self._removeChannel(channel)
            self.send(f"PART {channel}" if '#' in channel else f"PART#{channel}")

    def sendMessage(self, channelName: str, messageString: str)->None:
        """
        sendMessage - sends a message to channel
        
        :param channelName: Name of channel to send message
        :type channelName: str
        :param messageString: message to send
        :type messageString: str
        """
        self.send(f"PRIVMSG {'#' if '#' not in channelName else ''}{channelName} :{messageString}")

    def sendWhisper(self, channelName: str, username: str, messageString: str)->None:
        """
         sendWhisper - sends whisper to user in chat
        
        :param channelName: Name of channel to send message
        :type channelName: str
        :param username: Username to whisper
        :type username: str
        :param messageString: message to send
        :type messageString: str
        """
        self.send(f"PRIVMSG {'#' if '#' not in channelName else ''}{channelName} :/w {username} {messageString}")

    def clearMessage(self, message: Message):
        self.sendMessage(message.channel, f"/delete {message.id}")
       
       
    def timeoutUser(self, channelName: str, username: str, duration: int)->None:
        """
        timeoutUser - times user in channel
        
        :param channelName: name of channel
        :type channel: str
        :param username:  username of person 
        :type username: str
        :param duration: how long to timeout
        :type duration: int
        """
        self.send(f"PRIVMSG #{'#' if '#' not in channelName else ''}{channelName} :/timeout {username} {duration}")
   
    def onMessage(self, func)->None:
        """
        onMessage - message event - adds callback function for event 
        event object is of type class Message_
        
        :param func: The function to call on this event 
        :type func: a function or method
        """
       
        self._event.on(self._COMMANDS.MESSAGE, func)
    
    def onWhisper(self, func):
        """
        onWhisper - Whisper event - adds callback function for event 
        event object is of type class Message_
        
        :param func: The function to call on this event 
        :type func: a function or method
        """
        self._event.on(self._COMMANDS.WHISPER, func)

    def onRoomState(self, func):
        """
        onRoomState [summary]
        
        :param func: [description]
        :type func: [type]
        """
        self._event.on(self._COMMANDS.ROOMSTATE, func)

    def onMsgId(self, msgid, func):
        """
        onMsgId  - msgid events - adds callback to a given msgid
        event object is of type class Message
        
        :param msgid: https://dev.twitch.tv/docs/irc/msg-id or **TCI.COMMANDS.MESSAGEIDS**
        :type msgid: str
        :param func: The function to call on this event 
        :type func: a function or method
        """
        self._event.on(msgid, func)
        
    
    def onNotice(self, func):
        """
        onNotice [summary]
        
        :param func: [description]
        :type func: [type]
        """
        self._event.on(self._COMMANDS.NOTICE, func)

    def onReceived(self, func):
        """
        onReceived [summary]
        
        :param func: [description]
        :type func: [type]
        """
        self._event.on(self._COMMANDS.RECEIVED, func)


    def onConnected(self, func: Callable):
        """
        onConnected[summary]
        
        :param func: [description]
        :type func: [type]
        """
        self._event.on(self._COMMANDS.CONNECTED, func)
    
    def onDisconnected(self, func):
        """
        onConnected[summary]
        
        :param func: [description]
        :type func: [type]
        """
        self._event.on(self._COMMANDS.DISCONNECTED, func)


    def onLoginError(self, func):
        """
        onLoginError [summary]
        
        :param func: [description]
        :type func: [type]
        """
        self._event.on(self._COMMANDS.LOGIN_UNSUCCESSFUL, func)

    def onGlobalUSerState(self, func):
        """
        onGlobalUSerState [summary]
        
        :param func: [description]
        :type func: [type]
        """
        print("GOLBAALUSER EVENT")
        self._event.on(self._COMMANDS.GLOBALUSERSTATE, func)

    def onUserState(self, func):
        """
        onUserState [summary]
        
        :param func: [description]
        :type func: [type]
        """
        self._event.on(self._COMMANDS.USERSTATE, func)
    
    def onUserNotice(self, func):
        """
        onUserNotice [summary]
        
        :param func: [description]
        :type func: [type]
        """
        self._event.on(self._COMMANDS.USERNOTICE, func)

    def onEmotesOnlyOn(self, func):
        """[summary]
        
        :param func: [description]
        :type func: [type]
        """
        self._event.on(self._COMMANDS.ROOMSTATE.EMOTE_ONLY_ON, func)

    def onEmotesOnlyOff(self, func):
        """[summary]
        
        :param func: [description]
        :type func: [type]
        """
        self._event.on(self._COMMANDS.ROOMSTATE.EMOTE_ONLY_OFF, func)

    def onSubsOnlyOn(self, func):
        """[summary]
        
        :param func: [description]
        :type func: [type]
        """
        self._event.on(self._COMMANDS.ROOMSTATE.SUBS_ONLY_ON, func)

    def onSubsOnlyOff(self, func):
        """[summary]
        
        :param func: [description]
        :type func: [type]
        """
        self._event.on(self._COMMANDS.ROOMSTATE.SUBS_ONLY_OFF, func)  

    def onFollersOnlyOn(self, func):
        """[summary]
        
        :param func: [description]
        :type func: [type]
        """
        self._event.on(self._COMMANDS.ROOMSTATE.FOLLOWERS_ONLY_ON, func)
    
    def onFollersOnlyOff(self, func):
        """[summary]
        
        :param func: [description]
        :type func: [type]
        """
        self._event.on(self._COMMANDS.ROOMSTATE.FOLLOWERS_ONLY_OFF, func)

    def onSlowModeOn(self, func):
        """[summary]
        
        :param func: [description]
        :type func: [type]
        """
        self._event.on(self._COMMANDS.ROOMSTATE.SLOW_ON, func)

    def onSlowModeOff(self, func):
        """[summary]
        
        :param func: [description]
        :type func: [type]
        """
        self._event.on(self._COMMANDS.ROOMSTATE.SLOW_OFF, func)

    def onJoin(self, func: Callable):
        self._event.on(self._COMMANDS.JOIN, func)