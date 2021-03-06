.\" {PTM/WK/1999-11-22}
.\"	$OpenBSD: mktemp.1,v 1.5 1997/06/17 15:34:27 millert Exp $
.\"
.\" Copyright (c) 1989, 1991, 1993
.\"	The Regents of the University of California.  All rights reserved.
.\"
.\" Redistribution and use in source and binary forms, with or without
.\" modification, are permitted provided that the following conditions
.\" are met:
.\" 1. Redistributions of source code must retain the above copyright
.\"    notice, this list of conditions and the following disclaimer.
.\" 2. Redistributions in binary form must reproduce the above copyright
.\"    notice, this list of conditions and the following disclaimer in the
.\"    documentation and/or other materials provided with the distribution.
.\" 3. All advertising materials mentioning features or use of this software
.\"    must display the following acknowledgement:
.\"	This product includes software developed by the University of
.\"	California, Berkeley and its contributors.
.\" 4. Neither the name of the University nor the names of its contributors
.\"    may be used to endorse or promote products derived from this software
.\"    without specific prior written permission.
.\"
.\" THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
.\" ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
.\" IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
.\" ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
.\" FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
.\" DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
.\" OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
.\" HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
.\" LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
.\" OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
.\" SUCH DAMAGE.
.\"
.Dd November, 20, 1996
.Dt MKTEMP 1
.Os
.Sh NAZWA
.Nm mktemp
.Nd tw�rz unikaln� nazw� pliku tymczasowego
.Sh SK�ADNIA
.Nm mktemp
.Op Fl d
.Op Fl q
.Op Fl u
.Ar wzorzec
.Sh OPIS
Narz�dzie
.Nm mktemp
pobiera zadany wzorzec nazwy i zast�puje jego cz�� by stworzy�
nazw� pliku. Wynikowa nazwa jest unikalna i nadaje si� do u�ywania jako
nazwa pliku.
Wzorzec mo�e by�
.\" ---- Nie jest prawd� dla Linuksa, ale w libc z OpenBSD
.\" dowolna nazwa pliku z pewn� liczb�
dowoln� nazw� pliku z dodanymi do niej dok�adnie sze�cioma znakami
.\" ----
.Ql X ,
na przyk�ad
.\" .Pa /tmp/temp.XXXX .
.Pa /tmp/temp.XXXXXX .
Ko�cowe
.Ql X
zast�powane s� przez numer bie��cego procesu i/lub unikaln� kombinacj� liter.

Liczba unikalnych nazw plik�w, jakie mo�e zwr�ci�
.Nm
.\" ---- Nie jest prawd� dla Linuksa, ale dla libc z OpenBSD
.\" mo�e zwr�ci� zale�y od liczby dodanych
.\" .Ql X �w;
.\" sze��
.\" .Ql X �w
.\" da przetestowanie oko�o 26 ** 6 kombinacji.
daje oko�o 26 ** 6 kombinacji.
.\" ----
.Pp
Je�li
.Nm
mo�e pomy�lnie utworzy� unikaln� nazw� pliku, to tworzony jest plik
z prawami 0600 (chyba �e podano flag�
.Fl u )
za� nazwa pliku wy�wietlana jest na standardowym wyj�ciu.
.Sh OPCJE
.Bl -tag -width indent
Dost�pne s� nast�puj�ce opcje:
.It Fl d
Utw�rz katalog zamiast pliku.
.It Fl q
Ciche zako�czenie dzia�ania w przypadku b��du. Przydatne, gdy skrypt nie
chce by komunikat o b��dzie trafi� na standardowe wyj�cie b��d�w.
.It Fl u
Dzia�aj w trybie
.Dq unsafe
(ryzykownym).
Plik tymczasowy b�dzie skasowany (unlinked) przed zako�czeniem pracy
.Nm mktemp .
Jest to nieco lepsze ni�
.Fn mktemp 3 ,
ale nadal wprowadza `race condition' [t�um: ``wy�cig'' proces�w
pomi�dzy uzyskiwaniem unikalnych nazw i nadawaniem ich plikom].
Nie zaleca si� u�ywania tej opcji.
.Sh ZWRACANE WARTO�CI
Narz�dzie
.Nm
ko�czy prac� z warto�ci� 0 w przypadku powodzenia, za� 1 przy b��dzie.
.Sh PRZYK�ADY
Poni�szy fragment w 
.Xr sh 1
ilustruje proste zastosowanie
.Nm mktemp ,
gdzie skrypt winien zako�czy� prac� je�li nie mo�e utworzy� bezpiecznego
pliku tymczasowego.
.Bd -literal -offset indent
TMPFILE=`mktemp /tmp/$0.XXXXXX` || exit 1
echo "program output" >> $TMPFILE
.Ed
.Pp
W tym przypadku chcemy, by skrypt sam obs�ugiwa� b��d.
.Bd -literal -offset indent
TMPFILE=`mktemp -q /tmp/$0.XXXXXX`
if [ $? -ne 0 ]; then
	echo "$0: Can't create temp file, exiting..."
	exit 1
fi
.Ed
.Pp
Zauwa�, �e mo�na te� zamiast sprawdzania $? sprawdza�,
czy $TMPFILE ma d�ugo�� zerow�. Pozwala to na wykonanie
sprawdzenia w dalszej cz�ci skryptu (gdy� $? zostanie
nadpisane przez nast�pne polecenie  pow�oki).
.Sh ZOBACZ TAK�E
.Xr mkstemp 3 ,
.Xr mktemp 3 .
.Sh HISTORIA
Narz�dzie
.Nm
pojawi�o si� w
.Bx Open .
