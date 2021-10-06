打造一款属于自己的终端配置,方案就是「zsh」+「oh my zsh」+「powerlevel10k」。

## 参考资料
   * 资料1 [用「zsh」「oh my zsh」「powerlevel10k」,打造属于你的终端环境](https://www.jianshu.com/p/7162c4b7a438)
   * 资料2 [愉快的工作,从舒适的终端开始!](https://zhuanlan.zhihu.com/p/80139116)
## Linux下的安装
1. 现在已经可以直接通过终端来直接安装zsh了
    ```
    sudo apt-get install zsh
    ```
2. 然后可以查看zsh版本
   ```
    zsh --version
   ```
3. 将zsh设置成默认,取代默认的bash
   ```
   sudo chsh -s /bin/zsh
   ```
4. 安装oh my zsh,这里使用wget安装
   ```
   sh -c "$(wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"
   ```
5. 安装powerlevel0k,他比powerlevel9k性能快上10-100倍
   ```
   git clone https://github.com/romkatv/powerlevel10k.git $ZSH_CUSTOM/themes/powerlevel10k
   ```
   成功安装powerlevel10k后,需要修改~/.zshrc里面的**ZSH_THEME**变量
   ```
   vim ~/.zshrc
   ```
   然后修改成如下面这样
   ```
   ZSH_THEME=powerlevel10k/powerlevel10k
   ```
   **设置好后,保存退出。关闭终端,重启终端,如果是第一次安装Powerlevel0k主题的话,会启动设置向导来设置Powerlevel10k的配置,跟着问题走回答问题就可以了。全部回答完后,会自动修改~/.zshrc里面的配置。**
   
6. 安装Nerd-fonts字体,这个字体应该是支持字形最多的了,有近1G大小。
   
   先git到本地
   ```
   git clone https://github.com/ryanoasis/nerd-fonts.git --depth 1
   ```
   然后用脚本安装,然后删除nerd-fonts目录
   ```
   cd nerd-fonts
   ./install.sh
   cd ..
   rm -rf nerd-fonts
   ```
   最后在~/.zshrc里面添加下面一句就算结束了。
   ```
   POWERLEVEL9K_MODE='nerdfont-complete'
   ```

## Mac OS下的安装
1. Mac OS下默认已经安装zsh了,可以直接使用。
   
   可以查看下zsh版本,然后设置默认终端为zsh。
   ```
   zsh --version
   sudo chsh -s /bin/zsh
   ```

2. 安装oh my zsh,这里使用curl。
   ```
   sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
   ```

3. 安装powerlevel0k。
   ```
   git clone https://github.com/romkatv/powerlevel10k.git $ZSH_CUSTOM/themes/powerlevel10k
   ```
   修改~/.zshrc里面的**ZSH_THEME**变量
   ```
   ZSH_THEME=powerlevel10k/powerlevel10k
   ```
   **设置好后,保存退出。关闭终端,重启终端,如果是第一次安装Powerlevel0k主题的话,会启动设置向导来设置Powerlevel10k的配置,跟着问题走回答问题就可以了。全部回答完后,会自动修改~/.zshrc里面的配置。**

4. 安装Nerd-fonts字体
   先git到本地
   ```
   git clone https://github.com/ryanoasis/nerd-fonts.git --depth 1
   ```
   然后用脚本安装,然后删除nerd-fonts目录
   ```
   cd nerd-fonts
   ./install.sh
   cd ..
   rm -rf nerd-fonts
   ```
   最后在~/.zshrc里面添加下面一句就算结束了
   ```
   POWERLEVEL9K_MODE='nerdfont-complete'
   ```