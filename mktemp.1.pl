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
.Nd twórz unikaln± nazwê pliku tymczasowego
.Sh SK£ADNIA
.Nm mktemp
.Op Fl d
.Op Fl q
.Op Fl u
.Ar wzorzec
.Sh OPIS
Narzêdzie
.Nm mktemp
pobiera zadany wzorzec nazwy i zastêpuje jego czê¶æ by stworzyæ
nazwê pliku. Wynikowa nazwa jest unikalna i nadaje siê do u¿ywania jako
nazwa pliku.
Wzorzec mo¿e byæ
.\" ---- Nie jest prawd± dla Linuksa, ale w libc z OpenBSD
.\" dowolna nazwa pliku z pewn± liczb±
dowoln± nazw± pliku z dodanymi do niej dok³adnie sze¶cioma znakami
.\" ----
.Ql X ,
na przyk³ad
.\" .Pa /tmp/temp.XXXX .
.Pa /tmp/temp.XXXXXX .
Koñcowe
.Ql X
zastêpowane s± przez numer bie¿±cego procesu i/lub unikaln± kombinacjê liter.

Liczba unikalnych nazw plików, jakie mo¿e zwróciæ
.Nm
.\" ---- Nie jest prawd± dla Linuksa, ale dla libc z OpenBSD
.\" mo¿e zwróciæ zale¿y od liczby dodanych
.\" .Ql X ów;
.\" sze¶æ
.\" .Ql X ów
.\" da przetestowanie oko³o 26 ** 6 kombinacji.
daje oko³o 26 ** 6 kombinacji.
.\" ----
.Pp
Je¶li
.Nm
mo¿e pomy¶lnie utworzyæ unikaln± nazwê pliku, to tworzony jest plik
z prawami 0600 (chyba ¿e podano flagê
.Fl u )
za¶ nazwa pliku wy¶wietlana jest na standardowym wyj¶ciu.
.Sh OPCJE
.Bl -tag -width indent
Dostêpne s± nastêpuj±ce opcje:
.It Fl d
Utwórz katalog zamiast pliku.
.It Fl q
Ciche zakoñczenie dzia³ania w przypadku b³êdu. Przydatne, gdy skrypt nie
chce by komunikat o b³êdzie trafi³ na standardowe wyj¶cie b³êdów.
.It Fl u
Dzia³aj w trybie
.Dq unsafe
(ryzykownym).
Plik tymczasowy bêdzie skasowany (unlinked) przed zakoñczeniem pracy
.Nm mktemp .
Jest to nieco lepsze ni¿
.Fn mktemp 3 ,
ale nadal wprowadza `race condition' [t³um: ``wy¶cig'' procesów
pomiêdzy uzyskiwaniem unikalnych nazw i nadawaniem ich plikom].
Nie zaleca siê u¿ywania tej opcji.
.Sh ZWRACANE WARTO¦CI
Narzêdzie
.Nm
koñczy pracê z warto¶ci± 0 w przypadku powodzenia, za¶ 1 przy b³êdzie.
.Sh PRZYK£ADY
Poni¿szy fragment w 
.Xr sh 1
ilustruje proste zastosowanie
.Nm mktemp ,
gdzie skrypt winien zakoñczyæ pracê je¶li nie mo¿e utworzyæ bezpiecznego
pliku tymczasowego.
.Bd -literal -offset indent
TMPFILE=`mktemp /tmp/$0.XXXXXX` || exit 1
echo "program output" >> $TMPFILE
.Ed
.Pp
W tym przypadku chcemy, by skrypt sam obs³ugiwa³ b³±d.
.Bd -literal -offset indent
TMPFILE=`mktemp -q /tmp/$0.XXXXXX`
if [ $? -ne 0 ]; then
	echo "$0: Can't create temp file, exiting..."
	exit 1
fi
.Ed
.Pp
Zauwa¿, ¿e mo¿na te¿ zamiast sprawdzania $? sprawdzaæ,
czy $TMPFILE ma d³ugo¶æ zerow±. Pozwala to na wykonanie
sprawdzenia w dalszej czê¶ci skryptu (gdy¿ $? zostanie
nadpisane przez nastêpne polecenie  pow³oki).
.Sh ZOBACZ TAK¯E
.Xr mkstemp 3 ,
.Xr mktemp 3 .
.Sh HISTORIA
Narzêdzie
.Nm
pojawi³o siê w
.Bx Open .
