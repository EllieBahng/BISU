# 部署指南：同学状态摸底问卷

## 整体流程

```
Supabase（存数据）→ GitHub 推代码 → Vercel（自动部署）→ 分享链接
```

---

## 第一步：Supabase 建数据库

1. 打开 [supabase.com](https://supabase.com)，注册/登录（免费）
2. 点 **New project**，填写项目名（如 `survey`），选一个地区（推荐 Singapore）
3. 等待项目创建完成（约1分钟）
4. 点左侧 **SQL Editor**，把下面这段 SQL 全部粘贴进去，点 **Run**：

```sql
create table responses (
  id bigserial primary key,
  created_at timestamptz default now(),
  name text,
  class_name text,
  direction text,
  anxiety_level text,
  wants_chat text,
  contact text,
  message text,
  full_answers jsonb
);

-- 允许匿名提交（学生不需要登录）
alter table responses enable row level security;
create policy "允许提交" on responses for insert to anon with check (true);
create policy "服务端读取" on responses for select using (auth.role() = 'service_role');
```

5. 获取两个密钥（**Settings → API**）：
   - **URL**：形如 `https://xxxx.supabase.co`
   - **anon public**：学生提交用
   - **service_role secret**：老师查看用（点 Reveal 才能看到）

---

## 第二步：修改 index.html 填入 Supabase 信息

打开 `public/index.html`，找到第 109-110 行：

```javascript
const SUPABASE_URL = 'YOUR_SUPABASE_URL';
const SUPABASE_KEY = 'YOUR_SUPABASE_ANON_KEY';
```

替换成你的真实值：

```javascript
const SUPABASE_URL = 'https://xxxx.supabase.co';
const SUPABASE_KEY = 'eyJxxx...（anon key）';
```

---

## 第三步：推代码到 GitHub

仓库地址：`https://github.com/EllieBahng/BISU`

```bash
# 进入项目目录
cd "C:\Users\I774154\Desktop\脚本\survey-v2"

# 初始化 git（如果还没有）
git init
git remote add origin https://github.com/EllieBahng/BISU.git

# 推代码
git add .
git commit -m "add survey v2"
git push -u origin main
```

---

## 第四步：Vercel 部署

1. 打开 [vercel.com](https://vercel.com)，用 GitHub 账号登录
   - 注意：Vercel 连的是 github.com，SAP 内网 GitHub 可能无法直连
   - **如果连不上**：在 [github.com](https://github.com) 新建一个公开仓库，把代码推到那里，再用 Vercel 部署

2. 点 **Add New → Project**，选择你的仓库
3. Framework Preset 选 **Other**，不需要改其他设置
4. 点 **Deploy**，等待约1分钟

---

## 第五步：设置环境变量（重要！）

部署完成后，进入项目 → **Settings → Environment Variables**，添加 3 个：

| 变量名 | 值 |
|---|---|
| `SUPABASE_URL` | `https://xxxx.supabase.co` |
| `SUPABASE_SERVICE_KEY` | （service_role key，长字符串） |
| `RESULTS_PASSWORD` | 你设置的老师查看密码，如 `wangjinming2025` |

添加完毕后点 **Redeploy** 让环境变量生效。

---

## 完成后

- **学生答题链接**：`https://你的项目名.vercel.app/`
- **老师查看链接**：`https://你的项目名.vercel.app/results`（输入你设置的密码）

两个链接都是永久可用的，不依赖你的电脑。

---

## 常见问题

**问：学生提交后我多久能看到？**  
答：实时的，刷新结果页就能看到。

**问：Vercel 免费版有限制吗？**  
答：每月 100GB 流量，问卷这种用量完全够，几年内不用担心。

**问：数据会丢吗？**  
答：Supabase 免费版数据永久保存，不会丢。

**问：如果 SAP GitHub 连不上 Vercel 怎么办？**  
答：在 github.com 注册一个普通账号，把 survey-v2 整个文件夹推上去，再用 Vercel 连那个仓库部署即可。Supabase 的数据不受影响。
