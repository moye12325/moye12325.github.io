---
date: 2024-07-22T17:49:50.927Z
updated: null
title: Navicat查看密码
slug: '954818659'
oid: 669e9bbe2a6fe84dfe9209f5
categories: 所遇问题
type: post
permalink: /posts/所遇问题/954818659
---


# Navicat中怎么查看数据库密码

1. 第一步:导出链接，导出连接，获取到connections.ncx 文件，勾选导出密码

![](https://qiniu.kanes.top/blog/Navicat查看密码_image_1.png)
![](https://qiniu.kanes.top/blog/Navicat查看密码_image_2.png)

2. 第二步：找到加密密码，进行破解

在导出的connections.ncx文件中找到password，然后复制出来。
![](https://qiniu.kanes.top/blog/Navicat查看密码_image_3.png)

打开这个网址：[https://tool.lu/coderunner](https://tool.lu/coderunner)，将如下刚刚密码复制进去，

$[decode](https://so.csdn.net/so/search?q=decode&spm=1001.2101.3001.7020) = $navicatPassword->decrypt('复制出来的密码');

```php
<?php
class NavicatPassword
{
    protected $version = 0;
    protected $aesKey = 'libcckeylibcckey';
    protected $aesIv = 'libcciv libcciv ';
    protected $blowString = '3DC5CA39';
    protected $blowKey = null;
    protected $blowIv = null;
     
    public function __construct($version = 12)
    {
        $this->version = $version;
        $this->blowKey = sha1('3DC5CA39', true);
        $this->blowIv = hex2bin('d9c7c3c8870d64bd');
    }
     
    public function encrypt($string)
    {
        $result = FALSE;
        switch ($this->version) {
            case 11:
                $result = $this->encryptEleven($string);
                break;
            case 12:
                $result = $this->encryptTwelve($string);
                break;
            default:
                break;
        }
         
        return $result;
    }
     
    protected function encryptEleven($string)
    {
        $round = intval(floor(strlen($string) / 8));
        $leftLength = strlen($string) % 8;
        $result = '';
        $currentVector = $this->blowIv;
         
        for ($i = 0; $i < $round; $i++) {
            $temp = $this->encryptBlock($this->xorBytes(substr($string, 8 * $i, 8), $currentVector));
            $currentVector = $this->xorBytes($currentVector, $temp);
            $result .= $temp;
        }
         
        if ($leftLength) {
            $currentVector = $this->encryptBlock($currentVector);
            $result .= $this->xorBytes(substr($string, 8 * $i, $leftLength), $currentVector);
        }
         
        return strtoupper(bin2hex($result));
    }
     
    protected function encryptBlock($block)
    {
        return openssl_encrypt($block, 'BF-ECB', $this->blowKey, OPENSSL_RAW_DATA|OPENSSL_NO_PADDING);
    }
     
    protected function decryptBlock($block)
    {
        return openssl_decrypt($block, 'BF-ECB', $this->blowKey, OPENSSL_RAW_DATA|OPENSSL_NO_PADDING);
    }
     
    protected function xorBytes($str1, $str2)
    {
        $result = '';
        for ($i = 0; $i < strlen($str1); $i++) {
            $result .= chr(ord($str1[$i]) ^ ord($str2[$i]));
        }
         
        return $result;
    }
     
    protected function encryptTwelve($string)
    {
        $result = openssl_encrypt($string, 'AES-128-CBC', $this->aesKey, OPENSSL_RAW_DATA, $this->aesIv);
        return strtoupper(bin2hex($result));
    }
     
    public function decrypt($string)
    {
        $result = FALSE;
        switch ($this->version) {
            case 11:
                $result = $this->decryptEleven($string);
                break;
            case 12:
                $result = $this->decryptTwelve($string);
                break;
            default:
                break;
        }
         
        return $result;
    }
     
    protected function decryptEleven($upperString)
    {
        $string = hex2bin(strtolower($upperString));
         
        $round = intval(floor(strlen($string) / 8));
        $leftLength = strlen($string) % 8;
        $result = '';
        $currentVector = $this->blowIv;
         
        for ($i = 0; $i < $round; $i++) {
            $encryptedBlock = substr($string, 8 * $i, 8);
            $temp = $this->xorBytes($this->decryptBlock($encryptedBlock), $currentVector);
            $currentVector = $this->xorBytes($currentVector, $encryptedBlock);
            $result .= $temp;
        }
         
        if ($leftLength) {
            $currentVector = $this->encryptBlock($currentVector);
            $result .= $this->xorBytes(substr($string, 8 * $i, $leftLength), $currentVector);
        }
         
        return $result;
    }
     
    protected function decryptTwelve($upperString)
    {
        $string = hex2bin(strtolower($upperString));
        return openssl_decrypt($string, 'AES-128-CBC', $this->aesKey, OPENSSL_RAW_DATA, $this->aesIv);
    }
};
 
 
//需要指定版本两种，11或12
//$navicatPassword = new NavicatPassword(11);
//这里我指定的12的版本，原先指定的11，执行之后的密码是乱码
$navicatPassword = new NavicatPassword(12);
 
//解密
//$decode = $navicatPassword->decrypt('15057D7BA390');
$decode = $navicatPassword->decrypt('复制出来的密码');
echo $decode."\n";
?>
```

然后在网页上面执行代码，就可以得到密码了
![](https://qiniu.kanes.top/blog/Navicat查看密码_image_4.png)