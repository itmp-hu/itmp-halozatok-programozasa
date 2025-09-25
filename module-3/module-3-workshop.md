# 3. modul workshop - Hálózatprogramozás és automatizáció


1.) Készítsünk el egy adott könyvtárat, de csak ha a "cisco" felhasználó létezik!

<details>
<summary style="border-left: 2px solid lightgray; padding: 5px; font-style:italic">A feladat részletes megoldása</summary>

```yaml
---
- name: Create /tmp/exists directory if user "cisco" exists
  hosts: all
  become: yes
  tasks:
    - name: Check if user "cisco" exists
      command: id cisco
      register: user_check
      ignore_errors: true		# akkor is folytatja, ha hiba van
    - name: Create /tmp/exists directory if user "cisco" exists
      file:
        path: /tmp/exists
        state: directory
      when: user_check.rc == 0	# rc: return code

```

</details>

2.) Másoljunk ki egy adott fájlt minden Linux gép adott könyvtárába!

<details>
<summary style="border-left: 2px solid lightgray; padding: 5px; font-style:italic">A feladat részletes megoldása</summary>

```yaml
---
- name: File-ok kimasolasa a gepekre
  hosts: linux
  become: yes
  become_user: root
  tasks:
    - name: file masolasa
      copy:
        src: /home/devasc/forras.txt
        dest: /home/cisco/forras.txt

```

</details>

3.) Módosítsuk a /etc/sudoers fájlt!

<details>
<summary style="border-left: 2px solid lightgray; padding: 5px; font-style:italic">A feladat részletes megoldása</summary>

```yaml
---
- name: Konfig fajl modositasa
  hosts: all
  become: yes
  become_user: root
  tasks:
    - name: cmnd_alias beszurasa
      lineinfile:
        path: /etc/sudoers
        state: present
        regexp: '^# Cmnd '
        insertafter: '^# Cmnd '
        line: 'Cmnd_Alias NETPROGS = /usr/bin/ip, /usr/bin/nmtui'
    - name: cisco usernek alias adasa
      lineinfile:
        path: /etc/sudoers
        state: present
        line: 'cisco ALL=(ALL:ALL) NOPASSWD: NETPROGS'

```

</details>

4.) Kapcsoljuk be a jelszótitkosítást

<details>
<summary style="border-left: 2px solid lightgray; padding: 5px; font-style:italic">A feladat részletes megoldása</summary>

```yaml
---
- name: Make users
    hosts: all
    become: yes
    gather_facts: no
    tasks:
    - name: Making users
        user:
        name: "{{ item }}"
        group: users
        password: '$5$uLm2j7pL7yP$5o6BSUvNoyqmCfUlLmyK0T5mboF3P1O3x93wHOgbH7C'
        shell: /bin/bash
        comment: User "{{ item }}"
        loop:
        - tercsi
        - fercsi
        - kata
        - klara

```

</details>
