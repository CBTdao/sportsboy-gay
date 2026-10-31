<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:atom="http://www.w3.org/2005/Atom">
  <xsl:output method="html" encoding="UTF-8" indent="yes" doctype-system="about:legacy-compat"/>

  <xsl:template match="/">
    <html lang="zh-CN">
      <head>
        <meta charset="UTF-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title><xsl:value-of select="rss/channel/title"/> · 追更</title>
        <style>
          :root { --bg:#0E0D0B; --surface:#16140F; --line:#2a2620; --coral:#FF5C39; --text:#f3efe6; --muted:#a79f92; }
          * { box-sizing:border-box; }
          body { margin:0; background:var(--bg); color:var(--text);
                 font-family:"Noto Sans SC",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
                 line-height:1.7; padding:0 0 64px; }
          .wrap { max-width:760px; margin:0 auto; padding:0 20px; }
          header { padding:40px 20px 24px; text-align:center; border-bottom:1px solid var(--line); }
          .brand { font-weight:900; letter-spacing:.04em; font-size:14px; color:var(--muted); }
          .brand b { color:var(--coral); }
          h1 { font-size:28px; margin:14px 0 6px; }
          .sub { color:var(--muted); font-size:15px; }
          .note { background:var(--surface); border:1px solid var(--line); border-radius:12px;
                  padding:14px 16px; margin:28px 0; font-size:14px; color:var(--muted); }
          .note code { background:#000; color:var(--coral); padding:2px 8px; border-radius:6px;
                       font-family:ui-monospace,Menlo,Consolas,monospace; word-break:break-all; }
          ul { list-style:none; padding:0; margin:0; display:grid; gap:16px; }
          li { background:var(--surface); border:1px solid var(--line); border-radius:14px; padding:18px 20px;
               transition:border-color .18s; }
          li:hover { border-color:var(--coral); }
          li a { color:var(--text); text-decoration:none; font-size:19px; font-weight:700; }
          li a:hover { color:var(--coral); }
          .date { display:block; color:var(--muted); font-size:12px; margin:4px 0 8px; }
          li p { margin:0; color:var(--muted); font-size:15px; }
          .back { display:inline-block; margin-top:28px; color:var(--coral); text-decoration:none;
                  font-weight:700; border-bottom:1px dashed var(--coral); }
          footer { text-align:center; color:var(--muted); font-size:12px; margin-top:40px; }
        </style>
      </head>
      <body>
        <header>
          <div class="brand">SPORTSBOY<b>.gay</b></div>
          <h1><xsl:value-of select="rss/channel/title"/></h1>
          <div class="sub">追更页面 · 每天更新一场，自动送达</div>
        </header>
        <div class="wrap">
          <div class="note">
            把下面这个地址添加到你的 RSS 阅读器（Feedly、鲜果、NetNewsWire、手机订阅器均可），
            之后每发布新章都会自动出现在你的订阅里：<br/>
            <code><xsl:value-of select="rss/channel/atom:link/@href"/></code>
          </div>

          <ul>
            <xsl:for-each select="rss/channel/item">
              <li>
                <a href="{link}"><xsl:value-of select="title"/></a>
                <span class="date"><xsl:value-of select="pubDate"/></span>
                <p><xsl:value-of select="description"/></p>
              </li>
            </xsl:for-each>
          </ul>

          <a class="back" href="/vn">← 返回《体育生》连载首页</a>

          <footer>汗水、肌肉与骄傲，光明正大。本站内容均为成年人设定。</footer>
        </div>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
