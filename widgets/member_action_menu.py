# widgets/member_action_menu.py

from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty

Builder.load_file('widgets/member_action_menu.kv')

class MemberActionMenu(Popup):
    member_id = NumericProperty(0)
    on_edit_callback = ObjectProperty(lambda mid: print(f"[WARN] Edit callback not set for member {mid}"))
    on_delete_callback = ObjectProperty(lambda mid: print(f"[WARN] Delete callback not set for member {mid}"))