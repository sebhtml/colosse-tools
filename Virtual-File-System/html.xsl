<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
  <html>
  <body>
    <h2>Items</h2>
    <table border="1">
      <tr bgcolor="#9acd32">
        <th>Item</th>
        <th>Value</th>
      </tr>
      <xsl:for-each select="objects/object">
      <tr>
        <td><xsl:value-of select="handle" /></td>
        <td><xsl:value-of select="score" /></td>
      </tr>
      </xsl:for-each>
    </table>
  </body>
  </html>
</xsl:template>
</xsl:stylesheet>


