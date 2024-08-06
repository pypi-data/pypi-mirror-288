# Common datatypes are encoded as dataclasses which behave like dicts but have fixed keys.
# In addition, string literals are encoded. This avoids "magic strings" appearing everywhere in the code.

import dataclasses
from dataclasses import dataclass
from typing import Optional, Any

BUTTON = "button"
CANVAS = "canvas"
SERVICE = "service"
FETCH_CHARACTERS = "fetch_characters"
FETCH_BUTTONS = "fetch_buttons"
FETCH_CANVAS = "fetch_canvas"
FETCH_STYLE = "fetch_style"
JOIN_CHANNEL = "join_channel"
LEAVE_CHANNEL = "leave_channel"
FETCH_CONTEXT_MENU = "fetch_context_menu"
FETCH_CHANNEL_INFO = "fetch_channel_info"
UPDATE = "update"
UPDATE_CHARACTERS = "update_characters"
UPDATE_CHANNEL_INFO = "update_channel_info"
UPDATE_CANVAS = "update_canvas"
UPDATE_BUTTONS = "update_buttons"
UPDATE_STYLE = "update_style"
UPDATE_CONTEXT_MENU = "update_context_menu"
USER_LOGIN = "user_login"
SERVICE_LOGIN = "service_login"
HEARTBEAT = "heartbeat" # Action subtypes.
ROGER = "roger"
COPY = "copy"
IGNORE = "ignore"
UNBIND = "unbind"
INCLUDE = "include"
BUTTON_CLICK = "button_click"
MENU_CLICK = "menu_click"
MESSAGE_UP = "message_up"
MESSAGE_DOWN = "message_down"
ACTION = "action"
TEXT = "text" # Message subtypes.
IMAGE = "image"
AUDIO = "audio"
FILE = "file"
CARD = "card"
IMAGE_EXTS = {'.jpe', '.jpg', '.jpeg', '.gif', '.png', '.bmp', '.ico', '.svg', '.svgz', '.tif', '.tiff', '.ai', '.drw', '.pct', '.psp', '.xcf', '.raw', '.webp', '.heic'}
AUDIO_EXTS = {'.wav', '.mp3', '.mp4', '.mp5'} # .mp5 became popular around 2030.


def add_str_method(cls):
  """Decorator function to make __str__ return the following format:
     "Foo(bar=1, baz='two', etc)"; only the non-default or specified fields are included.
     This works given a class to decorate.
     Returns the decorated function.
     """
  #Example from https://stackoverflow.com/questions/71344648/how-to-define-str-for-dataclass-that-omits-default-values
  def __str__(self):
    s = ', '.join(f'{field.name}={getattr(self, field.name)}'
                  for field in dataclasses.fields(self)
                  if getattr(self, field.name) != field.default)
    ty = 'moobius.'+type(self).__name__.split('.')[-1]
    return f'{ty}({s})'

  setattr(cls, '__str__', __str__)
  setattr(cls, '__repr__', __str__)
  return cls


@dataclass
@add_str_method
class ButtonArgument:
    """Describes pop-up menus inside of buttons. Such buttons have "arguments" as a list of ButtonArguments.
    Not used if the button does not contain a pop-up menu."""
    name: str # The app-specified ID of the argument.
    type: str # What kind of box the user sees; "string" | "enum"
    optional: Optional[bool] # Can the user skip it?
    placeholder: str # A hint to the user.
    values: Optional[list[str]]=None # What values are available, if the type is enum. Use None if the type is str.


@dataclass
@add_str_method
class BottomButton:
    """Buttons appearing at the bottom of pop-up menus."""
    text: str # The button text.
    type: str # The button type.


@dataclass
@add_str_method
class Button:
    """A description of a button. These buttons appear above the chat-box."""
    button_id: str # The app-specified ID of the button was pressed.
    button_name: str # The text which appears in the browser.
    new_window: bool # Does the button open up a menu to select options in?
    arguments: Optional[list[ButtonArgument]]=None # If new_window, what arguments appear in the pop-up.
    bottom_buttons:Optional[list[BottomButton]]=None # If new_window, what buttons appear at the bottom of the pop-up.


@dataclass
@add_str_method
class ButtonClickArgument:
    """Describes which option users clicked on in a pop-up menu.
    A ButtonClick will have a list of ButtonClickArguments if the button opens up a pop-up menu.
    Also used, uncommonly, for context-menu clicks which use pop-up submenus.
    Not used if the button does not contain a pop-up menu."""
    name: str # The ButtonArgument ID this applies to.
    value: str | int # The choice itself. Int for the "enum" button type. String for the "string" button type.


@dataclass
@add_str_method
class ButtonClick:
    """A description of a button click. Who clicked on which button.
    And what arguments they picked, if the button opens a pop-up menu."""
    button_id: str # The Button ID this applies to.
    channel_id: str # What channel the user was in when the pressed the button.
    button_type: str # What kind of button was pressed (rarely used).
    sender: str # The Character ID of who clicked the button. Can be a real user or an agent.
    arguments: list[ButtonClickArgument] # What settings the user chosse (for buttons that open a pop-up menu).
    context: dict # Rarely used metadata.


@dataclass
@add_str_method
class ContextMenuElement:
    """One element of a right-click context menu. The full menu is described by a list of these elements."""
    item_id: str # The app-specified ID of the Element.
    item_name: str # What text to show in the browser.
    support_subtype: list[str] # What message types will open the context menu. ["text","file", etc].
    new_window: Optional[bool] = False # Does clicking this menu open it's own sub-menu (this is an advanced feature).
    arguments: Optional[list[ButtonArgument]] = None # If clicking this menu opens a sub-menu, what is inside said sub-menu.


@dataclass
@add_str_method
class MessageContent:
    """The content of a message. Most messages only have a single non-None item; for example "text" messages only have a "text" element.
    The exteption is "card" messages; they have links, title, and buttons."""
    text: Optional[str] = None # The string (for "text" messages).
    path: Optional[str] = None # The URL (for any non-text message).
    size: Optional[int] = None # The size in bytes, used for downloadable "file" messages only.
    filename: Optional[str] = None # The filename to display, used for downloadable "file" messages only.
    link: Optional[str] = None # The URL, used for "card" messages which have a clickable link.
    title: Optional[str] = None # The title shown, used for "card" messages which have a clickable link.
    button: Optional[str] = None # The text of the button shown, used for "card" messages which have a clickable link.


@dataclass
@add_str_method
class MenuClick:
    """A description of a context menu right-click. Includes a "copy" of the message that was clicked on."""
    item_id: str # The ContextMenuElement ID that this click applies to.
    message_id: str # The platform-generated ID of which message was clicked on (rarely used).
    message_subtype: str # The kind of message clicked on, 'text', 'image', 'audio', 'file', or 'card'.
    message_content: MessageContent # The content of the message that was clicked on.
    channel_id: str # The channel the user was in when they clicked the message.
    sender: str # The Character ID of the user or agent who clicked the message.
    recipients: list[str] # Rarely used.
    context: dict # Metadata rarely used.
    arguments: Optional[list[ButtonClickArgument]] = None # What sub-menu settings, if the menu element clicked on has a sub-menu.


@dataclass
@add_str_method
class CanvasElement:
    """A description of a canvas element. The full canvas description is a list of these elements."""
    text: Optional[str] = None # The text displayed.
    path: Optional[str] = None # The URL of the displayed image.


@dataclass
@add_str_method
class View:
    """An unused feature, for now."""
    character_ids: list[str] # List of Character IDs.
    button_ids: list[str] # List of Button ids.
    canvas_id: str # The platform-generated Canvas ID.


@dataclass
@add_str_method
class Group:
    """A group of users. Only to be used internally."""
    group_id: str # The platform-generated Group ID, used internally to send messages.
    character_ids: list[str] # A list of character ids who belong to this group.


@dataclass
@add_str_method
class MessageBody:
    """A message. Contains the content as well as who, when, and where the message was sent."""
    subtype: str # What kind of message it is; "text", "image", "audio", "file", or "card".
    channel_id: str # The Channel ID of the channel the message was sent in.
    content: MessageContent # The content of the message.
    timestamp: int # When the message was sent.
    recipients: list[str] # The Character IDs of who the message was sent to.
    sender: str # The Character ID of who sent the message.
    message_id: str | None # The platform-generated ID of the message itself. Rarely used.
    context: dict | None # Metadata that is rarely used.


@dataclass
@add_str_method
class Action:
    """A description of a generic task performed by a user. Actions with different subtypes are routed to different callbacks."""
    subtype: str # The subtype of the action. Used internally to route the action to the correct callback function.
    channel_id: str # The Channel ID of the channel the action is in.
    sender: str # The Character ID of who did the action.
    context: Optional[dict] # Rarely used metadata.


@dataclass
@add_str_method
class ChannelInfo:
    """A decription of an update for an old, rarely-used feature."""
    channel_id: str # The Channel ID of this channel.
    channel_name: str # The name of the channel, as appears in the list of channels.
    channel_description: str # A description that ideally should give information about what the channel is about.
    channel_type: str # An enum with "dcs", "ccs", etc. Rarely used.


@dataclass
@add_str_method
class Copy:
    """Used internally for the on_copy_client() callback. Most CCS apps do not need to override the callback."""
    request_id: str # Just a platform-generated ID to differentiate different copies.
    origin_type: str # What kind of data this copy comes from.
    status: bool # Rarely used.
    context: dict # Rarely used metadata.


@dataclass
@add_str_method
class Payload:
    """A description of a payload received from the websocket. Used internally by the Moobius.handle_received_payload function."""
    type: str # The kind of payload, used internally to route the payload to the correct callback function.
    request_id: Optional[str] # A platform-generated ID to differentiate payloads.
    user_id: Optional[str] # The Character ID of who dispatched this payload.
    body: MessageBody | ButtonClick | Action | Copy | MenuClick | Any # The body of the payload.


@dataclass
@add_str_method
class Character:
    """A description (name, id, image url, etc) of a real or puppet user."""
    character_id: str # The platform-generated ID of the character. Both for real and puppet users.
    name: str # The name as appears in the group chat.
    avatar: Optional[str] = None # The image the character has.
    description: Optional[str] = None # Information about who this Character is.
    character_context: Optional[dict] = None # Rarely used metadata.


@dataclass
@add_str_method
class StyleElement:
    """A description of a visual style element. The full visual style description is a list of these elements."""
    widget: str # The type of widget. Typically "CANVAS" but other widgets.
    display: str # Is it visible? "invisible", "visible", or "highlight"
    expand: Optional[bool] = None # Should the canvas be expanded? Only used for visible.
    button_id: Optional[str] = None # What button does this apply to?
    text: Optional[str] = None # What text, if any, does this apply do?


@dataclass
@add_str_method
class UpdateElement:
    """A single update of something. A description of an update is a list of these elements.
    Most fields are None, only one is non-None at a given time."""
    character: Character | None # The new Character. Only used if a character is bieng updated.
    button: Button | None # The new Button. Only used if a Button is bieng updated.
    channel_info: ChannelInfo | None # The new ChanelInfo. Only used if a Channel is bieng updated.
    context_menu_element: ContextMenuElement | None # The new ContextMenuElement. Only used if the right-click menu is bieng updated.
    canvas_element: CanvasElement | None # The new CanvasElement. Only used if the Canvas is bieng updated.
    style_element: StyleElement | None # The new StyleElement. Only used if an element's look and feel is bieng changed.


@dataclass
@add_str_method
class Update:
    """
    A description of an update. Includes update elements as well as who sees the update.
    Used for on_update_xyz callbacks. Not used for the send_update functions.
    This is sent to agents to notify them that something that they can "see" has been updated.
    """
    subtype:str # What is bieng updated, route the Update to the correct callback function. Such as 'update_characters', 'update_channel_info', 'update_canvas', 'update_buttons', 'update_style', etc.
    channel_id:str # The Channel ID of the channel this Update is in.
    content: list[UpdateElement] # The list of indivual changes in this update.
    context:dict # Rarely used metadata.
    recipients:list[str] # The list of Character IDs of who sees this update.
    group_id: Optional[str]=None # The Group ID of the group of users/agents who see this update.


@dataclass
@add_str_method
class UserInfo:
    """A description of a user profile.
    This is sent to agents so that they can learn about "themselves"."""
    avatar:str # The URL to the image shown in the group chat.
    description:str # A description of who this user is.
    name:str # The user's name.
    email:str # The user's email.
    email_verified:str # Did the user check thier email and click that link?
    user_id:str # The platform-generated Character ID for this user.
    system_context:Optional[dict]=None # Rarely-used metadata.
