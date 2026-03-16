#!/usr/bin/env python3
"""Unified CLI for the PingCode Codex skill."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from pingcode_client import PingCodeClient, PingCodeError


def add_common_output_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--raw", action="store_true", help="输出原始 JSON 响应")


def print_json(payload: Any) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def first_value(payload: dict[str, Any]) -> dict[str, Any]:
    values = payload.get("values")
    if isinstance(values, list) and values:
        first = values[0]
        if isinstance(first, dict):
            return first
    return payload


def cmd_list_projects(client: PingCodeClient, args: argparse.Namespace) -> None:
    payload = client.list_projects(args.identifier)
    if args.raw:
        print_json(payload)
        return
    values = payload.get("values", [])
    total = payload.get("total", len(values))
    print(f"项目总数: {total}")
    for item in values:
        print(f"- {item.get('name', 'N/A')} [{item.get('identifier', 'N/A')}] id={item.get('id', 'N/A')}")


def cmd_get_task(client: PingCodeClient, args: argparse.Namespace) -> None:
    payload = client.get_task(args.identifier)
    if args.raw:
        print_json(payload)
        return
    item = first_value(payload)
    print(f"任务: [{item.get('identifier', 'N/A')}] {item.get('title', 'N/A')}")
    print(f"ID: {item.get('id', 'N/A')}")
    project = item.get("project", {})
    if isinstance(project, dict):
        print(f"项目ID: {project.get('id', 'N/A')}")
    item_type = item.get("type", {})
    type_name = item_type.get("name", "N/A") if isinstance(item_type, dict) else item_type
    print(f"类型: {type_name}")
    description = item.get("description")
    if description:
        print(f"描述: {description}")


def cmd_create_project(client: PingCodeClient, args: argparse.Namespace) -> None:
    payload = client.create_project(args.name, args.identifier, args.type, args.description, args.visibility)
    if args.raw:
        print_json(payload)
        return
    print(f"已创建项目: {payload.get('name', 'N/A')}")
    print(f"项目ID: {payload.get('id', 'N/A')}")
    print(f"标识符: {payload.get('identifier', 'N/A')}")
    print(f"可见性: {payload.get('visibility', 'N/A')}")


def cmd_create_work_item(client: PingCodeClient, args: argparse.Namespace) -> None:
    payload = client.create_work_item(args.project_id, args.title, args.type, args.description, args.parent_id)
    if args.raw:
        print_json(payload)
        return
    item_type = payload.get("type", {})
    type_name = item_type.get("name", "N/A") if isinstance(item_type, dict) else item_type
    print(f"已创建工作项: [{payload.get('identifier', 'N/A')}] {payload.get('title', 'N/A')}")
    print(f"类型: {type_name}")
    print(f"ID: {payload.get('id', 'N/A')}")


def cmd_update_work_item(client: PingCodeClient, args: argparse.Namespace) -> None:
    payload = client.update_work_item(
        args.work_item_id,
        title=args.title,
        description=args.description,
        type_id=args.type,
        parent_id=args.parent_id,
        state_id=args.state_id,
    )
    if args.raw:
        print_json(payload)
        return
    item_type = payload.get("type", {})
    type_name = item_type.get("name", "N/A") if isinstance(item_type, dict) else item_type
    print(f"已更新工作项: [{payload.get('identifier', 'N/A')}] {payload.get('title', 'N/A')}")
    print(f"类型: {type_name}")
    print(f"ID: {payload.get('id', 'N/A')}")


def cmd_get_members(client: PingCodeClient, args: argparse.Namespace) -> None:
    payload = client.get_project_members(args.project_id)
    if args.raw:
        print_json(payload)
        return
    values = payload.get("values", [])
    total = payload.get("total", len(values))
    print(f"成员总数: {total}")
    for item in values:
        role = item.get("role", {})
        role_name = role.get("name", "N/A") if isinstance(role, dict) else role
        item_type = item.get("type", "user")
        if item_type == "user_group":
            group = item.get("user_group", {})
            print(f"- 组 {group.get('name', 'N/A')} role={role_name} id={group.get('id', 'N/A')}")
            continue
        user = item.get("user", {})
        label = user.get("display_name") or user.get("name") or "N/A"
        email = user.get("email")
        extra = f" email={email}" if email else ""
        print(f"- 用户 {label} role={role_name} id={user.get('id', 'N/A')}{extra}")


def cmd_add_member(client: PingCodeClient, args: argparse.Namespace) -> None:
    payload = client.add_project_member(args.project_id, args.user_id, args.role_id)
    if args.raw:
        print_json(payload)
        return
    print(f"已添加成员，记录ID: {payload.get('id', 'N/A')}")


def cmd_update_member(client: PingCodeClient, args: argparse.Namespace) -> None:
    payload = client.update_project_member(args.project_id, args.member_id, args.role_id)
    if args.raw:
        print_json(payload)
        return
    print(f"已更新成员角色，记录ID: {payload.get('id', 'N/A')}")


def cmd_remove_member(client: PingCodeClient, args: argparse.Namespace) -> None:
    payload = client.remove_project_member(args.project_id, args.member_id)
    if args.raw:
        print_json(payload)
        return
    print(f"已移除成员，记录ID: {payload.get('id', args.member_id)}")


def cmd_breakdown_story(client: PingCodeClient, args: argparse.Namespace) -> None:
    payload = client.get_task(args.identifier)
    item = first_value(payload)
    item_type = item.get("type", {})
    type_name = item_type.get("name", "") if isinstance(item_type, dict) else str(item_type)
    if type_name.lower() not in {"story", "用户故事"}:
        raise PingCodeError(f"目标工作项类型为 {type_name or '未知'}，不是可拆解子任务的 story。")

    title = item.get("title", args.identifier)
    work_item_id = item.get("id")
    project = item.get("project", {})
    project_id = project.get("id") if isinstance(project, dict) else None
    if not work_item_id or not project_id:
        raise PingCodeError("响应缺少父工作项 ID 或项目 ID，无法创建子任务。")

    subtasks = [
        (f"{title} - 需求分析", "分析需求边界、验收条件和依赖项"),
        (f"{title} - 技术方案", "输出实现方案、风险点和接口设计"),
        (f"{title} - 开发实现", "完成核心功能编码与必要联调"),
        (f"{title} - 测试验证", "补充测试用例并完成回归验证"),
    ]
    created: list[dict[str, Any]] = []
    for subtask_title, description in subtasks:
        created.append(
            client.create_work_item(
                project_id=project_id,
                title=subtask_title,
                type_id="task",
                description=description,
                parent_id=work_item_id,
            )
        )

    if args.raw:
        print_json({"parent": item, "created": created})
        return
    print(f"已为 [{item.get('identifier', 'N/A')}] {title} 创建 {len(created)} 个子任务:")
    for created_item in created:
        print(f"- [{created_item.get('identifier', 'N/A')}] {created_item.get('title', 'N/A')}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PingCode Codex skill CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_projects = subparsers.add_parser("list-projects", help="列出项目")
    list_projects.add_argument("--identifier", help="按项目标识符筛选")
    add_common_output_flags(list_projects)
    list_projects.set_defaults(func=cmd_list_projects)

    get_task = subparsers.add_parser("get-task", help="读取任务详情")
    get_task.add_argument("--identifier", required=True, help="工作项标识符，如 DEMO-123")
    add_common_output_flags(get_task)
    get_task.set_defaults(func=cmd_get_task)

    create_project = subparsers.add_parser("create-project", help="创建项目")
    create_project.add_argument("--name", required=True)
    create_project.add_argument("--identifier", required=True)
    create_project.add_argument("--type", default="scrum")
    create_project.add_argument("--description", default="")
    create_project.add_argument("--visibility", default="private")
    add_common_output_flags(create_project)
    create_project.set_defaults(func=cmd_create_project)

    create_work_item = subparsers.add_parser("create-work-item", help="创建工作项")
    create_work_item.add_argument("--project-id", required=True)
    create_work_item.add_argument("--title", required=True)
    create_work_item.add_argument("--type", default="task")
    create_work_item.add_argument("--description", default="")
    create_work_item.add_argument("--parent-id")
    add_common_output_flags(create_work_item)
    create_work_item.set_defaults(func=cmd_create_work_item)

    update_work_item = subparsers.add_parser("update-work-item", help="更新工作项")
    update_work_item.add_argument("--work-item-id", required=True)
    update_work_item.add_argument("--title")
    update_work_item.add_argument("--type")
    update_work_item.add_argument("--description")
    update_work_item.add_argument("--parent-id")
    update_work_item.add_argument("--state-id")
    add_common_output_flags(update_work_item)
    update_work_item.set_defaults(func=cmd_update_work_item)

    get_members = subparsers.add_parser("get-members", help="读取项目成员")
    get_members.add_argument("--project-id", required=True)
    add_common_output_flags(get_members)
    get_members.set_defaults(func=cmd_get_members)

    add_member = subparsers.add_parser("add-member", help="添加项目成员")
    add_member.add_argument("--project-id", required=True)
    add_member.add_argument("--user-id", required=True)
    add_member.add_argument("--role-id")
    add_common_output_flags(add_member)
    add_member.set_defaults(func=cmd_add_member)

    update_member = subparsers.add_parser("update-member", help="更新成员角色")
    update_member.add_argument("--project-id", required=True)
    update_member.add_argument("--member-id", required=True)
    update_member.add_argument("--role-id", required=True)
    add_common_output_flags(update_member)
    update_member.set_defaults(func=cmd_update_member)

    remove_member = subparsers.add_parser("remove-member", help="移除项目成员")
    remove_member.add_argument("--project-id", required=True)
    remove_member.add_argument("--member-id", required=True)
    add_common_output_flags(remove_member)
    remove_member.set_defaults(func=cmd_remove_member)

    breakdown_story = subparsers.add_parser("breakdown-story", help="把 story 拆成标准子任务")
    breakdown_story.add_argument("--identifier", required=True)
    add_common_output_flags(breakdown_story)
    breakdown_story.set_defaults(func=cmd_breakdown_story)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    client = PingCodeClient()
    try:
        args.func(client, args)
    except PingCodeError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
