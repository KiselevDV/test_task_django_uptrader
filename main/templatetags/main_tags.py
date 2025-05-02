from django import template
from django.utils.http import unquote
from urllib.parse import urlparse

from main.models import MenuItem


register = template.Library()


def normalize_path(path):
    """Убирать лишние / и query string"""
    parsed = urlparse(path)
    return parsed.path.rstrip('/') + '/'


def build_tree(items):
    """Простроить дерево пунктов меню из списка"""
    items_by_id = {item.id: item for item in items}
    for item in items:
        item.absolute_url = item.get_absolute_url()
        item.children_list = []
    for item in items:
        if item.parent_id:
            parent = items_by_id.get(item.parent_id)
            if parent:
                parent.children_list.append(item)
    # Корневые элементы и словарь id → item
    return [item for item in items if not item.parent_id], items_by_id


def get_active_ids(active_item, items_by_id):
    """Получить множество id активного пункта и его предков"""
    active_ids = set()
    while active_item:
        active_ids.add(active_item.id)
        active_item = items_by_id.get(active_item.parent_id)
    return active_ids


@register.inclusion_tag('main/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    """Template tag, определить активный пункт по request.path"""
    request = context['request']
    current_path = normalize_path(unquote(request.path))
    items = MenuItem.objects \
        .filter(menu__name=menu_name) \
        .select_related('parent') \
        .order_by('parent_id', 'id')
    list_items = list(items)
    root_items, items_by_id = build_tree(list_items)
    url_map = {normalize_path(item.absolute_url): item for item in list_items}
    active_item = url_map.get(current_path)
    active_ids = get_active_ids(active_item, items_by_id) if active_item else set()
    return {'menu_items': root_items, 'active_ids': active_ids}
