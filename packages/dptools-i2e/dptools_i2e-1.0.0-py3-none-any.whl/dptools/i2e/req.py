true = True
false = False


def create(space: str):
    return {
        "annotations": [
            {
                "name": f"space{space}::business_key",
                "value": "user_id"
            },
            {
                "name": f"space{space}::description_key",
                "value": "display_name"
            },
            {
                "name": f"space{space}::type_info",
                "value": "{\"tagList\":\"[\"BusinessObject\",\"SystemUser\"]\",\"type\":\"BUILTIN\",\"typeList\":\"[\"SYSTEM\"]\"}"
            }
        ],
        "links": [
            {
                "alias": "created_by",
                "from": "user_id",
                "name": "created_by",
                "relation": f'"public"."space{space}_md_os_user',
                "required": false,
                "source": "user_id",
                "target": "created_by",
                "to": "user_id",
                "type": f"space{space}::SystemUser"
            },
            {
                "alias": "changed_by",
                "from": "user_id",
                "name": "changed_by",
                "relation": f'"public"."space{space}_md_os_user',
                "required": false,
                "source": "user_id",
                "target": "changed_by",
                "to": "user_id",
                "type": f"space{space}::SystemUser"
            }
        ],
        "module": f"space{space}",
        "name": "SystemUser",
        "properties": [
            {
                "annotations": [
                    {
                        "name": "std::description",
                        "value": "{\"en\":\"user_id\", \"zh-cn\":\"用户ID\"}"
                    }
                ],
                "exclusive": true,
                "name": "user_id",
                "required": true,
                "type": "str"
            },
            {
                "annotations": [
                    {
                        "name": "std::description",
                        "value": "{\"en\":\"space\", \"zh-cn\":\"空间ID\"}"
                    }
                ],
                "name": "space",
                "type": "str"
            },
            {
                "annotations": [
                    {
                        "name": "std::description",
                        "value": "{\"en\":\"username\", \"zh-cn\":\"用户名\"}"
                    }
                ],
                "exclusive": true,
                "name": "username",
                "required": true,
                "type": "str"
            },
            {
                "annotations": [
                    {
                        "name": "std::description",
                        "value": "{\"en\":\"nickname\", \"zh-cn\":\"昵称\"}"
                    }
                ],
                "name": "nickname",
                "type": "str"
            },
            {
                "annotations": [
                    {
                        "name": "std::description",
                        "value": "{\"en\":\"display_name\", \"zh-cn\":\"显示名称\"}"
                    }
                ],
                "expr": "(.nickname ?? .username)",
                "name": "display_name",
                "type": "str"
            },
            {
                "annotations": [
                    {
                        "name": "std::description",
                        "value": "{\"en\":\"status\", \"zh-cn\":\"用户状态\"}"
                    },
                    {
                        "name": f"space{space}::enum_desc",
                        "value": "[{\"code\":\"ENABLE\",\"default\":true,\"name\":{\"en\":\"ENABLE\",\"zh-cn\":\"启用\"}},{\"code\":\"DISABLE\",\"default\":false,\"name\":{\"en\":\"DISABLE\",\"zh-cn\":\"禁用\"}}]"
                    }
                ],
                "name": "status",
                "type": "str"
            },
            {
                "annotations": [
                    {
                        "name": "std::description",
                        "value": "{\"en\":\"mobile_phone\", \"zh-cn\":\"移动电话\"}"
                    }
                ],
                "name": "mobile_phone",
                "type": "str"
            },
            {
                "annotations": [
                    {
                        "name": "std::description",
                        "value": "{\"en\":\"email\", \"zh-cn\":\"邮箱\"}"
                    }
                ],
                "name": "email",
                "type": "str"
            },
            {
                "annotations": [
                    {
                        "name": "std::description",
                        "value": "{\"en\":\"avatar\", \"zh-cn\":\"头像\"}"
                    }
                ],
                "name": "avatar",
                "type": "str"
            },
            {
                "annotations": [
                    {
                        "name": "std::description",
                        "value": "{\"en\":\"color\", \"zh-cn\":\"头像颜色\"}"
                    }
                ],
                "name": "color",
                "type": "str"
            },
            {
                "annotations": [
                    {
                        "name": "std::description",
                        "value": "{\"en\":\"sso_user\", \"zh-cn\":\"是否为sso用户\"}"
                    }
                ],
                "name": "sso_user",
                "type": "bool"
            },
            {
                "annotations": [
                    {
                        "name": "std::description",
                        "value": "{\"en\":\"created_time\", \"zh-cn\":\"创建时间\"}"
                    }
                ],
                "name": "created_time",
                "type": "timestamp"
            },
            {
                "annotations": [
                    {
                        "name": "std::description",
                        "value": "{\"en\":\"changed_time\", \"zh-cn\":\"更新时间\"}"
                    }
                ],
                "name": "changed_time",
                "type": "timestamp"
            },
            {
                "annotations": [
                    {
                        "name": "std::description",
                        "value": "{\"en\":\"username_modify_times\", \"zh-cn\":\"用户名修改次数\"}"
                    }
                ],
                "name": "username_modify_times",
                "type": "int2"
            },
            {
                "annotations": [
                    {
                        "name": "std::description",
                        "value": "{\"en\":\"is_active\", \"zh-cn\":\"是否有效\"}"
                    }
                ],
                "name": "is_active",
                "type": "bool"
            },
            {
                "annotations": [
                    {
                        "name": "std::description",
                        "value": "{\"en\":\"order\", \"zh-cn\":\"排序\"}"
                    }
                ],
                "name": "order",
                "type": "int2"
            },
            {
                "annotations": [
                    {
                        "name": "std::description",
                        "value": "{\"en\":\"is_myself\", \"zh-cn\":\"是否为当前用户\"}"
                    }
                ],
                "expr": f"(select .user_id = global space{space}::current_user_id)",
                "name": "is_myself"
            }
        ],
        "relation": f"(SELECT space, user_id, username, nickname, status, mobile_phone, email, avatar, is_active > 0 as is_active, \"order\", color, username_modify_times, sso_user > 0 as sso_user, created_by, changed_by, created_time, changed_time from public.space{space}_md_os_user) T0"
    }
