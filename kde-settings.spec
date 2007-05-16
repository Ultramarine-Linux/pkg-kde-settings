
%define rel 24

Summary: Config files for kde
Name:    kde-settings
Version: 3.5
Release: %{rel}%{?dist}

Group:   System Environment/Base
License: Public Domain
# This is a package which is specific to our distribution.  
# Thus the source is only available from within this srpm.
Source0: kde-settings-%{version}-%{rel}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires: kdelibs >= %{version}

Obsoletes: kde-config < %{version}-%{release}

%description
%{summary}.

%package kdm
Summary: Config files for kdebase(kdm)
Group:	 System Environment/Base
Obsoletes: kde-config-kdm < %{version}-%{release}
Requires: kdebase-kdm >= %{version}
%if 0%{?fedora} > 6 || 0%{?rhel} > 5
Requires: redhat-artwork-kde
%else
Requires: redhat-artwork
%endif
Requires: xorg-x11-xdm
%description kdm
%{summary}.


%prep
%setup -q -c -n %{name}

# fc6+ uses FedoraDNA
%if 0%{?fedora} > 5 
sed -i \
  -e "s|^Theme=.*|Theme=%{_datadir}/apps/kdm/themes/FedoraDNA|" \
  etc/kde/kdm/kdmrc
%endif

# fc7 uses FedoraFlyingHigh
%if 0%{?fedora} > 6
sed -i \
  -e "s|^ColorScheme=.*|ColorScheme=FedoraFlyingHigh|" \
  -e "s|^Theme=.*|Theme=%{_datadir}/apps/kdm/themes/FedoraFlyingHigh|" \
  etc/kde/kdm/kdmrc
%endif





%build
# Intentionally left blank.  Nothing to see here.


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{%{_datadir}/config,%{_sysconfdir}/kde/kdm}

tar cpf - etc/ usr/ | tar --directory $RPM_BUILD_ROOT -xvpf -

# kdebase/kdm symlink
rm -rf   $RPM_BUILD_ROOT%{_datadir}/config/kdm
ln -sf ../../../etc/kde/kdm $RPM_BUILD_ROOT%{_datadir}/config/kdm

# xdg_config_dirs-hack
#install -D -p -m755 %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/kde/env/xdg_env-hack.sh

touch %{name}.list

## NOTE: see also
## kdelibs: use FHS-friendly /etc/kde (vs. /usr/share/config), bug #238136
## can move items to /etc/kde when/if fixed.
for file in \
 $(find $RPM_BUILD_ROOT%{_sysconfdir}/kde -type f -maxdepth 1) \
 $(find $RPM_BUILD_ROOT%{_datadir}/config -type f -maxdepth 1) \
 ; do
  file_tmp=$(echo $file | sed -e "s|^$RPM_BUILD_ROOT||" )
  echo "%config(noreplace) $file_tmp" >> %{name}.list
done



%clean
rm -rf $RPM_BUILD_ROOT


## Use pre or triggerun kdebase ?  -- Rex
#triggerun kdebase < 6:3.5.5
#if [ $2 -gt 0 ]; then
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



%files 
%defattr(-,root,root,-)
%{_sysconfdir}/skel/.kde/
# drop noreplace, so we can be sure to get the new kiosk bits
%config %{_sysconfdir}/kderc
%{_datadir}/kde-settings/

%files kdm
%defattr(-,root,root,-)
#%{_sysconfdir}/kde/env/xdg_*-hack.sh
# compat symlink
%{_datadir}/config/kdm
%dir %{_sysconfdir}/kde/kdm
%config(noreplace) %{_sysconfdir}/kde/kdm/backgroundrc
%config(noreplace) %{_sysconfdir}/kde/kdm/kdmrc
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/kde/kdm/kdmrc.bak
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/kde/kdm/README*
%{_sysconfdir}/kde/kdm/Xaccess
%{_sysconfdir}/kde/kdm/Xresources
%{_sysconfdir}/kde/kdm/Xsession
%{_sysconfdir}/kde/kdm/Xwilling
%{_sysconfdir}/kde/kdm/Xservers
%{_sysconfdir}/kde/kdm/Xsetup
# hack needed for older rpm's
#exclude %{_sysconfdir}/X11/xdm/X*


%changelog
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

