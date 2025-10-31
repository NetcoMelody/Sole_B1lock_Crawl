# get_all_wp_users_paged.py
import xmlrpc.client
import csv
import sys

SITE_URL = "https://soleb1ock.com/xmlrpc.php"
USERNAME = "bigbiznb@gmail.com"
PASSWORD = "ZEqEeFo9SbCOZHJpZ84tNjq3"
OUTPUT_CSV = "wordpress_all_users.csv"
PER_PAGE = 100  # 每页数量（最大建议 50~100）


def main():
    print("正在连接 WordPress 站点...")
    server = xmlrpc.client.ServerProxy(SITE_URL)

    all_users = []
    offset = 0

    while True:
        try:
            # 使用 filter 分页获取
            filter_params = {
                'number': PER_PAGE,
                'offset': offset,
            }
            users = server.wp.getUsers(1, USERNAME, PASSWORD, filter_params)
        except xmlrpc.client.Fault as e:
            print(f"XML-RPC 错误: {e}")
            break
        except Exception as e:
            print(f"连接失败: {e}")
            break

        if not users:
            print(f"✅ 已获取全部用户，共 {len(all_users)} 人。")
            break

        all_users.extend(users)
        print(f"已获取 {len(all_users)} 个用户...")

        offset += PER_PAGE

    if not all_users:
        print("未获取到任何用户数据。")
        return

    # 写入 CSV
    fieldnames = [
        'user_id', 'username', 'email', 'first_name', 'last_name',
        'display_name', 'nickname', 'url', 'registered', 'roles'
    ]

    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for user in all_users:
            roles_str = ', '.join(user.get('roles', [])) if user.get('roles') else ''
            row = {
                'user_id': user.get('user_id'),
                'username': user.get('username'),
                'email': user.get('email'),
                'first_name': user.get('first_name'),
                'last_name': user.get('last_name'),
                'display_name': user.get('display_name'),
                'nickname': user.get('nickname'),
                'url': user.get('url'),
                'registered': user.get('registered'),
                'roles': roles_str
            }
            writer.writerow(row)

    print(f"✅ 所有用户信息已保存到 {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
