# THIS SPECFILE IS FOR F10+ ONLY!
# Sorry, it is just too different for conditionals to be worth it.
# The actuall tarball also DIFFERS between releases!
# Use kde-settings trunk for F10+, F-9 branch for F9, F-8 branch for F8.

%define rel 2

Summary: Config files for kde
Name:    kde-settings
Version: 4.1
Release: %{rel}%{?dist}

Group:   System Environment/Base
License: Public Domain
# This is a package which is specific to our distribution.  
# Thus the source is only available from within this srpm.
Source0: kde-settings-%{version}-%{rel}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

BuildRequires: kde-filesystem

Requires: kde-filesystem
# default (ok, inherited) icon theme
Requires: oxygen-icon-theme
# /etc/pam.d/ ownership
Requires: pam
Requires: xdg-user-dirs
# sed/kill used in gpg-agent-(startup/shutdown).sh
Requires: coreutils sed util-linux
# Solar theme for wallpaper, KSplash
Requires: solar-kde-theme

Requires(post): coreutils
Requires(postun): coreutils

Obsoletes: kde-config < %{version}-%{release}

%description
%{summary}.

%package kdm
Summary: Config files for kdebase-workspace(kdm)
Group:	 System Environment/Base
Obsoletes: kde-config-kdm < %{version}-%{release}
# Solar theme for KDM
Requires: solar-kde-theme
#Requires: kdebase-workspace
Requires: xorg-x11-xdm
Requires(pre): coreutils
Requires(post): coreutils grep sed
Requires(post): kde4-macros(api) = %{_kde4_macros_api}
%description kdm
%{summary}.

%package pulseaudio
Summary: Enable pulseaudio support in KDE
Group:   System Environment/Base
Requires: %{name} = %{version}-%{release}
Requires: pulseaudio
Requires: pulseaudio-module-x11
## kde3
Requires: alsa-plugins-pulseaudio
## kde4
Requires: xine-lib-pulseaudio
%description pulseaudio
%{summary}.


%prep
%setup -q -c -n %{name}


%build
# Intentionally left blank.  Nothing to see here.


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_datadir}/config,%{_sysconfdir}/kde/kdm}

tar cpf - etc/ usr/ | tar --directory %{buildroot} -xvpf -

# kdebase/kdm symlink
rm -rf   %{buildroot}%{_datadir}/config/kdm
ln -sf ../../../etc/kde/kdm %{buildroot}%{_datadir}/config/kdm


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_datadir}/kde-settings/kde-profile/default/share/icons/Fedora-KDE ||:

%postun
touch --no-create %{_datadir}/kde-settings/kde-profile/default/share/icons/Fedora-KDE ||:

%pre kdm
## KDM fixup(s)
# handle move from /etc/X11/xdm/kdmrc to /etc/kde/kdm/kdmrc
[ -L %{_sysconfdir}/kde/kdm/kdmrc ] && \
  %{__mv} -v %{_sysconfdir}/kde/kdm/kdmrc %{_sysconfdir}/kde/kdm/kdmrc.rpmorig ||:
# handle %%_datadir/config/kdm -> /etc/kde/kdm
[ -d %{_datadir}/config/kdm -a ! -L %{_datadir}/config/kdm ] && \
  %{__mv} -v %{_datadir}/config/kdm %{_datadir}/config/kdm.rpmorig ||:

%post kdm
## KDM fixup(s)
# handle move from /etc/X11/xdm/kdmrc to /etc/kde/kdm/kdmrc
[ ! -f %{_sysconfdir}/kde/kdm/kdmrc -a -f %{_sysconfdir}/kde/kdm/kdmrc.rpmnew ] && \
  %{__cp} -a %{_sysconfdir}/kde/kdm/kdmrc.rpmnew %{_sysconfdir}/kde/kdm/kdmrc ||:
# kdm v3 themes don't work (#444730)
# this hack assumes %_datadir != %_kde4_datadir
(grep "^Theme=%{_datadir}/apps/kdm/themes/" %{_sysconfdir}/kde/kdm/kdmrc > /dev/null && \
 sed -i -e "s|^Theme=%{_datadir}/apps/kdm/themes/.*|Theme=%{_kde4_appsdir}/kdm/themes/SolarMania|" \
 %{_sysconfdir}/kde/kdm/kdmrc
) ||:


%files 
%defattr(-,root,root,-)
%{_sysconfdir}/kde/env/env.sh
%{_sysconfdir}/kde/env/gpg-agent*.sh
%{_sysconfdir}/kde/env/fedora-bookmarks.sh
%{_sysconfdir}/kde/shutdown/gpg-agent*.sh
%config(noreplace) /etc/pam.d/kcheckpass
%config(noreplace) /etc/pam.d/kscreensaver
# drop noreplace, so we can be sure to get the new kiosk bits
%config %{_sysconfdir}/kderc
%config %{_sysconfdir}/kde4rc
%{_datadir}/kde-settings/

%files kdm
%defattr(-,root,root,-)
%config(noreplace) /etc/pam.d/kdm*
#%{_sysconfdir}/kde/env/xdg_*-hack.sh
# compat symlink
%{_datadir}/config/kdm
%dir %{_sysconfdir}/kde/kdm
%config(noreplace) %{_sysconfdir}/kde/kdm/backgroundrc
%config(noreplace) %{_sysconfdir}/kde/kdm/kdmrc
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/kde/kdm/README*
%{_sysconfdir}/kde/kdm/Xaccess
%{_sysconfdir}/kde/kdm/Xresources
%{_sysconfdir}/kde/kdm/Xsession
%{_sysconfdir}/kde/kdm/Xwilling
%{_sysconfdir}/kde/kdm/Xservers
%{_sysconfdir}/kde/kdm/Xsetup
# hack needed for older rpm's
#exclude %{_sysconfdir}/X11/xdm/X*

%files pulseaudio
%defattr(-,root,root,-)
# nothing, this is a metapackage


%changelog
* Mon Oct 27 2008 Jaroslav Reznik <jreznik@redhat.com> 4.1-2
- Fedoraproject homepages for Konqueror

* Sun Oct 26 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1-1
- default to Solar artwork

* Sat Sep 27 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0-29
- remove /etc/kde/env/pulseaudio.sh, no longer needed in F10 (#448477)

* Sat Sep 27 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0-28
- kxkbrc: set default keyboard model to evdev (matches F10+ X11 setup, #464101)

* Tue Sep 16 2008 Than Ngo <than@redhat.com> 4.0-27
- remove unneeded symlinks in Fedora-KDE icon theme

* Tue Sep 16 2008 Than Ngo <than@redhat.com> 4.0-26
- fix, systemsettings->icons doesn't show icons by Fedora-KDE
  icon theme

* Wed Jul 30 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-25
- kcminputrc: [Mouse] cursorTheme=default

* Tue May 20 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-24
- kdm pam settings need to sync with gdm (#447245)

* Fri May 16 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-23
- don't set XDG_CONFIG_DIRS (#249109)

* Thu May 01 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0-22.1
- use correct _kde4_appsdir for kdm theme upgrade hack (#444730)

* Thu May 01 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-22
- kdmrc: TerminateServer=true hack until Xserver fixed properly (#443307)
- %%post kdm: don't try to use old kde3 kdm themes (#444730)
- add/fix scriptlet deps

* Fri Apr 18 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-21
- kglobalshortsrc: add keyboard shortcuts for Virtual desktop switching (#440415)

* Fri Apr 11 2008 Than Ngo <than@redhat.com> 4.0-20
- set Fedora_Waves wallpaper theme default

* Thu Apr 10 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-19
- kmixrc: Visible=false
- ksmserverrc: start kmix (could use autostart for this too)
- kwalletrc: (sane defaults)

* Thu Apr 10 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-18
- kdmrc: [X-*-Greeter] Theme=FedoraWaves
- ksplashrc: [KSplash] Theme=FedoraWaves
- kdmrc: [Shutdown] BootManager=None (#441313)

* Wed Apr 09 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-17
- env.sh: XDG_CONFIG_DATA -> XDG_DATA_DIRS (oops)
- kdmrc: [X-*-Greeter] ColorScheme=ObsidianCoast
- include Fedora-KDE icon theme (#438973)
- kdeglobals: [Icons] Theme=Fedora-KDE (#438973)

* Mon Apr 07 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-16.1
- -pulseaudio: Requires: xine-lib-pulseaudio

* Mon Apr 07 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-16
- backgroundrc,kdmrc: first stab at F9/sulfur theming (#441167)
- kdmrc: ServerArgsLocal=-br (suggested by ajax)

* Thu Mar 27 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-15
- ksplashrc: [KSplash] Theme=Waves

* Thu Mar 20 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-14.1
- Requires: oxygen-icon-theme

* Tue Mar 11 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-14
- kde4rc: omit userProfileMapFile key

* Mon Mar 10 2008 Than Ngo <than@redhat.com> 4.0-13.1
- make oxygen the default windows manager

* Mon Mar 10 2008 Than Ngo <than@redhat.com> 4.0-12.1
- gestures disable as default
- omit kdesktoprc

* Sun Mar 09 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0-11.1
- symlink /etc/kderc to /etc/kde4rc

* Tue Feb 19 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-11
- kdmrc: BootManager=Grub (#374011)
- omit errant clock_pannelapplet_wkid..._rc (#431890)
- include (initially empty) applications/defaults.list
- env.sh: set XDG_CONFIG_DATA
- ksplashrc: disable FedoraInfinity (for now, doesn't work)
- kdeglobals: cleanup, set oxygen defaults mostly
- kickerrc 'n friends: nuke

* Fri Feb 15 2008 Than Ngo <than@redhat.com> 4.0-10
- added default bookmarks (imported from fedora-bookmarks),
  thanks Sebastian Vahl 

* Wed Jan 23 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-9.1
- include gpg-agent scripts here (#427316)

* Sat Jan 19 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.0-9
- kdeglobals: also set K3Spell_Client=4 and K3Spell_Encoding=11

* Thu Jan 10 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 4.0-8
- include /etc/kde/env/env.sh (#426115)
- move extra sources into tarball
- -kdm: cleanup deps

* Fri Jan 04 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 4.0-7
- omit legacy/crufy etc/skel bits
- -pulseaudio: -Requires: xine-lib-extras (too buggy)

* Sat Dec 22 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.0-6
- kdeglobals: KSpell_Client=4 (Hunspell), add KSpell_Encoding=11 (UTF-8)

* Wed Dec 12 2007 Than Ngo <than@redhat.com> 4.0-5
- add missing kdm-np pam, bz421931

* Fri Dec 07 2007 Than Ngo <than@redhat.com> 4.0-4
- kdmrc: ServerTimeout=30

* Wed Dec 05 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.0-3
- include pam configs
- -pulseaudio: +Requires: xine-lib-extras

* Tue Dec 04 2007 Than Ngo <than@redhat.com> 4.0-2
- kdmrc: circles as kdm default theme

* Mon Dec 03 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.0-1
- kdmrc: fix ClientLogFile and EchoMode->EchoPasswd for KDE 4 KDM
- kdmrc: disable Infinity theme (revert to circles), incompatible with KDE 4
- Require kde-filesystem instead of kdelibs3
- don't Require redhat-artwork

* Wed Oct 31 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 3.5-35
- kdeglobals: remove [WM] section, which overrides ColorScheme

* Mon Oct 29 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.5-34
- ksplashrc: Theme=FedoraInfinity (thanks to Chitlesh Goorah)

* Tue Oct 23 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 3.5-33.1
- -pulseaudio: new subpkg, to enable pulseaudio support

* Tue Oct 23 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 3.5-33
- kdmrc: ColorScheme=FedoraInfinityKDM
- ksplashrc: drop Theme=Echo (ie, revert to Default)
- kdeglobals: colorScheme=FedoraInfinity.kcsrc

* Tue Oct 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 3.5-32
- f8: Requires: fedorainfinity-kdm-theme (#314041)
      kdmrc: [X-*-Greeter] Theme=.../FedoraInfinity
      kdmrc: [X-*-Greeter] ColorScheme=FedoraInfinity

* Wed Sep 26 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 3.5-31
- kdesktoprc: [Desktop0] Wallpaper=/usr/share/backgrounds/images/default.png
  (#290571)
- kopeterc: [ContactList] SmoothScrolling=false

* Mon Jul 02 2007 Than Ngo <than@redhat.com> -  3.5-30
- fix bz#245100

* Mon Jun 18 2007 Than Ngo <than@redhat.com> -  3.5-29
- cleanup kde-setings, bz#242564

* Mon May 21 2007 Than Ngo <than@redhat.com> - 3.5-28
- don't hardcode locale in kdeglobals config
- cleanup clock setting
- plastik as default colorscheme
- use bzip2

* Fri May 18 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-27
- kdeglobals: [Icons] Theme = crystalsvg
- kdeglobals: [Paths] Trash[$e]=$(xdg-user-dir DESKTOP)/Trash/
- Requires: xdg-user-dirs

* Thu May 17 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-26
- omit kde-profile/default/share/icons

* Tue May 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-25
- ksplashrc does not contain Echo (#233881)
- kdmrc: MaxShowUID=65530, so we don't see nfsnobody
- kdmrc: HiddenUsers=root (MinShowUID=500 doesn't work?)

* Tue May 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-24
- omit FedoraFlyingHigh.kcsrc (it's now in redhat-artwork-kde)
- kdeglobals: xdg-user-dirs integration: Desktop, Documents (#238371)

* Tue May 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-23
- backgroundrc: Background=default.jpg 
- kderc: kioskAdmin=root:
- omit (previously accidentally included) alternative konq throbbers

* Tue May 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-21
- kiosk-style configs (finally)
- kdm use UserLists, FedoraFlyingHigh color scheme (#239701) 

* Tue May 01 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-20
- don't mix tab/spaces
- %%setup -q
- Source0 URL comment

* Mon Apr 30 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-19
- omit xdg_hack (for now)
- fc7+: Req: redhat-artwork-kde
- reference: kdelibs: use FHS-friendly /etc/kde (vs. /usr/share/config), bug #238136

* Wed Feb 14 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-18
- rename to kde-settings, avoid confusion with builtin %%_bindir/kde-config

* Wed Feb 14 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-17
- put back awol: Obsoletes/Provides: kde-config-kdebase

* Wed Jan 17 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-16
- kcmnspluginrc: scanPaths: +/usr/lib/firefox/plugins (flash-plugin-9 compat)

* Mon Jan 06 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-15
- xdg_env-hack: handle XDG_MENU_PREFIX too

* Fri Jan 05 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-14
- +Requires: kdelibs
- -kdm: +Requires: kdebase-kdm

* Fri Nov 17 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-13
- mv xdg_config_dirs-hack to env startup script instead of autostart konsole app.
- rename -kdebase -> -kdm
- drop circular dependency crud.

* Fri Oct 27 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-12
- %%exclude %%_datadir/config/kdm (from main pkg)
- ksmserverrc: loginMode=restoreSavedSession

* Fri Oct 27 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-10
- kwinrc: PluginLib=kwin_plastik (from kwin_bluecurve)
- xdg_config_dirs-hack: backup existing $HOME/.config/menus

* Thu Oct 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-7
- fixup %%pre/%%post to properly handle kdmrc move
- xdg_config_dirs-hack: don't run on *every* login

* Tue Oct 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-6
- xdg_config_dirs-hack: hack to force (re)run of kbuildsycoca if a
  change in $XDG_CONFIG_DIRS is detected. 

* Tue Oct 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-5
- kdmrc: prefer FedoraDNA,Bluecurve Themes respectively (if available)
- kdeglobals: (Icon) Theme=Bluecurve (minimize migration pain)

* Mon Oct 23 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-4
- kdeglobals: [Locale] US-centric defaults

* Tue Oct 17 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-3
- -kdebase: own %%_sysconfdir/kde/kdm, %%_datadir/config/kdm

* Wed Oct 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-2
- actually include something this time

* Wed Oct 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-1
- first try

