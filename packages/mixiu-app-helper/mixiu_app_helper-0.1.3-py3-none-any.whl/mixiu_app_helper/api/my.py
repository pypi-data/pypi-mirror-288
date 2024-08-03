# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-app-helper
# FileName:     my.py
# Description:  TODO
# Author:       zhouhanlin
# CreateDate:   2024/07/16
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from poco.proxy import UIObjectProxy
from airtest_helper.core import DeviceApi
from airtest_helper.platform import ANDROID_PLATFORM
from airtest_helper.libs.extend import get_poco_factory, get_poco_child


class MyApi(DeviceApi):

    def get_my(self, loop: int = 1, peroid: float = 0.5, **kwargs) -> UIObjectProxy:
        d_type = ""
        name = ""
        if self.platform == ANDROID_PLATFORM:
            d_type = "android.widget.TextView"
            name = "com.mixiu.com:id/tvTabItemText4"
        options = dict(d_type=d_type, name=name, text="我的")
        return get_poco_factory(poco=self.poco, options=options, loop=loop, peroid=peroid, **kwargs)

    def touch_my(self, loop: int = 1, peroid: float = 0.5, **kwargs) -> bool:
        my_poco = self.get_my(loop=loop, peroid=peroid, **kwargs)
        if my_poco:
            my_poco.click()
            return True
        return False

    def get_current_uid(self, loop: int = 1, peroid: float = 0.5, **kwargs) -> str:
        options = dict(d_type="android.widget.LinearLayout", name="com.mixiu.com:id/llUidAddress")
        parent_poco = get_poco_factory(poco=self.poco, options=options, loop=loop, peroid=peroid, **kwargs)
        if parent_poco:
            child_options = dict(name="android.widget.TextView")
            child_poco = get_poco_child(
                ui_object=parent_poco, options=child_options, child_index=1, loop=loop, peroid=peroid, **kwargs
            )
            if child_poco:
                return child_poco.get_text().strip()
        return ""
