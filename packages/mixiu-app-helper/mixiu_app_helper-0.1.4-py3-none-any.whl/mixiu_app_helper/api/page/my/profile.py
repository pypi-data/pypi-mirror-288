# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-app-helper
# FileName:     profile.py
# Description:  TODO
# Author:       zhouhanlin
# CreateDate:   2024/07/30
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from poco.proxy import UIObjectProxy
from airtest_helper.core import DeviceApi
from airtest_helper.platform import ANDROID_PLATFORM
from airtest_helper.libs.extend import get_poco_factory, get_poco_child


class UiProfileApi(DeviceApi):

    def get_my(self, loop: int = 20, peroid: float = 0.5, **kwargs) -> UIObjectProxy:
        d_type = ""
        name = ""
        if self.platform == ANDROID_PLATFORM:
            d_type = "android.widget.TextView"
            name = "com.mixiu.com:id/tvTabItemText4"
        options = dict(d_type=d_type, name=name, text="我的")
        return get_poco_factory(poco=self.poco, options=options, loop=loop, peroid=peroid, **kwargs)

    def touch_my(self, loop: int = 20, peroid: float = 0.5, **kwargs) -> bool:
        my_poco = self.get_my(loop=loop, peroid=peroid, **kwargs)
        if my_poco:
            my_poco.click()
            return True
        return False

    def get_user_uid(self, loop: int = 20, peroid: float = 0.5, **kwargs) -> int or None:
        options = dict(d_type="android.widget.LinearLayout", name="com.mixiu.com:id/llUidAddress")
        parent_poco = get_poco_factory(poco=self.poco, options=options, loop=loop, peroid=peroid, **kwargs)
        if parent_poco:
            child_options = dict(name="android.widget.TextView")
            child_poco = get_poco_child(
                ui_object=parent_poco, options=child_options, child_index=1, loop=loop, peroid=peroid, **kwargs
            )
            if child_poco:
                uid_str = child_poco.get_text().strip()
                return int(uid_str) if isinstance(uid_str, str) and uid_str.isdigit() is True else None
        return None

    def get_user_ip_location(self, loop: int = 20, peroid: float = 0.5, **kwargs) -> str or None:
        options = dict(d_type="android.widget.LinearLayout", name="com.mixiu.com:id/llUidAddress")
        parent_poco = get_poco_factory(poco=self.poco, options=options, loop=loop, peroid=peroid, **kwargs)
        if parent_poco:
            child_options = dict(name="android.widget.TextView")
            child_poco = get_poco_child(
                ui_object=parent_poco, options=child_options, child_index=3, loop=loop, peroid=peroid, **kwargs
            )
            if child_poco:
                return child_poco.get_text().strip()
        return None

    def get_user_diamond_balance(self, loop: int = 20, peroid: float = 0.5, **kwargs) -> int or None:
        options = dict(d_type="android.widget.TextView", name="com.mixiu.com:id/tvBlueDiamond")
        diamond_element = get_poco_factory(poco=self.poco, options=options, loop=loop, peroid=peroid, **kwargs)
        if diamond_element:
            diamond_str = diamond_element.get_text().strip()
            return int(diamond_str) if isinstance(diamond_str, str) and diamond_str.isdigit() is True else None
        return None

    def get_user_mi_bean_balance(self, loop: int = 20, peroid: float = 0.5, **kwargs) -> int or None:
        options = dict(d_type="android.widget.TextView", name="com.mixiu.com:id/tvCatCoin")
        cat_coin_element = get_poco_factory(poco=self.poco, options=options, loop=loop, peroid=peroid, **kwargs)
        if cat_coin_element:
            cat_coin_str = cat_coin_element.get_text().strip()
            return int(cat_coin_str) if isinstance(cat_coin_str, str) and cat_coin_str.isdigit() is True else None
        return None

    def get_user_fans(self, loop: int = 20, peroid: float = 0.5, **kwargs) -> int or None:
        options = dict(d_type="android.widget.TextView", name="com.mixiu.com:id/tvFansCount")
        fans_element = get_poco_factory(poco=self.poco, options=options, loop=loop, peroid=peroid, **kwargs)
        if fans_element:
            fans_str = fans_element.get_text().strip()
            return int(fans_str) if isinstance(fans_str, str) and fans_str.isdigit() is True else None
        return None

    def get_user_follow(self, loop: int = 20, peroid: float = 0.5, **kwargs) -> int or None:
        options = dict(d_type="android.widget.TextView", name="com.mixiu.com:id/tvFollowCount")
        follow_element = get_poco_factory(poco=self.poco, options=options, loop=loop, peroid=peroid, **kwargs)
        if follow_element:
            follow_str = follow_element.get_text().strip()
            return int(follow_str) if isinstance(follow_str, str) and follow_str.isdigit() is True else None
        return None

    def get_user_visitor(self, loop: int = 20, peroid: float = 0.5, **kwargs) -> int or None:
        options = dict(d_type="android.widget.TextView", name="com.mixiu.com:id/tvVisitorCount")
        visitor_element = get_poco_factory(poco=self.poco, options=options, loop=loop, peroid=peroid, **kwargs)
        if visitor_element:
            visitor_str = visitor_element.get_text().strip()
            return int(visitor_str) if isinstance(visitor_str, str) and visitor_str.isdigit() is True else None
        return None

    def get_user_name(self, loop: int = 20, peroid: float = 0.5, **kwargs) -> str or None:
        options = dict(d_type="android.widget.TextView", name="com.mixiu.com:id/tvUserName")
        user_name_element = get_poco_factory(poco=self.poco, options=options, loop=loop, peroid=peroid, **kwargs)
        if user_name_element:
            return user_name_element.get_text().strip()
        return None
