.\" 1999 PTM Przemek Borys
.\" Update: Robert Luberda <robert@debian.org>, Aug 2002, fileutils 4.1.10
.\" $Id$
.TH STAT "1" "lipiec 2002" "stat (fileutils) 4.1.10" "polecenia u¿ytkownika"
.SH NAZWA
stat \- drukuj status pliku lub systemu plików
.SH SK£ADNIA
.B stat
[\fIOPCJA\fR] \fIPLIK\fR...
.SH OPIS
.\" Add any additional description here
.PP
Wy¶wietla status pliku lub systemu plików
.TP
\fB\-f\fR, \fB\-\-filesystem\fR
wy¶wietla informacje o stanie systemu plików, a nie o stanie pliku
.TP
\fB\-c\fR  \fB\-\-format\fR=\fIFORMAT\fR
u¿ywa podanego FORMATU zamiast formatu domy¶lnego
.TP
\fB\-l\fR, \fB\-\-dereference\fR
pod±¿a za linkami
.TP
\fB\-t\fR, \fB\-\-terse\fR
wy¶wietla informacje w zwiêz³ej postaci
.TP
\fB\-\-help\fR
wy¶wietla pomoc i koñczy dzia³anie
.TP
\fB\-\-version\fR
wy¶wietla informacje o wersji i koñczy dzia³anie
.PP
Poprawne sekwencje formatu dla plików (je¿eli nie podano opcji \fB\-\-filesystem\fR):  
.IP
.\" doda³em pocz±tkowe spacje w liniach poni¿ej - dla zwiêkszenia czytelno¶ci (RL)
 %A - prawa dostêpu w formie czytelnej dla cz³owieka
 %a - prawa dostêpu ósemkowo
 %b - liczba zaalokowanych bloków
 %D - numer urz±dzenia szesnastkowo
 %d - numer urz±dzenia w systemie dziesiêtnym
 %F - typ pliku
 %f - tryb pliku szesnastkowo
 %G - nazwa grupy, która jest w³a¶cicielem pliku
 %g - identyfikator grupy, która jest w³a¶cicielem pliku
 %h - liczba twardych dowi±zañ
 %i - numer wêz³a (inode)
 %N - nazwa pliku w apostrofach ze wskazaniem linków symbol.
 %n - nazwa pliku
 %o - rozmiar bloku wej¶cia/wyj¶cia
 %s - ca³kowity rozmiar w bajtach
 %T - poboczny (minor) typ urz±dzenia szesnastkowo
 %t - g³ówny (major) typ urz±dzenia szesnastkowo
 %U - nazwa w³a¶ciciela pliku
 %u - identyfikator w³a¶ciciela pliku
 %X - czas ostatniego dostêpu podany jako liczba sekund od epoki
 %x - czas ostatniego dostêpu
 %Y - czas ostatniej modyfikacji jako liczba sekund od epoki
 %y - czas ostatniej modyfikacji
 %Z - czas ostatniej zmiany podany jako liczba sekund od epoki
 %z - czas ostatniej zmiany
.PP
Poprawne sekwencje formatu dla systemów plików:
.IP
 %a - liczba wolnych bloków dostêpnych dla nie-administratorów
 %b - ca³kowita liczba bloków danych w systemie plików
 %c - ca³kowita liczba wêz³ów w systemie plików
 %d - liczba wolnych wêz³ów w systemie plików
 %f - liczba wolnych bloków w systemie plików
 %i - identyfikator systemu plików szesnastkowo
 %l - maksymalna d³ugo¶æ nazw plików
 %n - nazwa pliku
 %s - optymalny rozmiar bloku przy transferze
 %T - typ w formie czytelnej dla cz³owieka
 %t - typ szesnastkowo
.SH AUTOR
Napisane przez Michaela Meskesa.
.SH "ZG£ASZANIE B£ÊDÓW"
Prosimy zg³aszaæ b³êdy do <bug-fileutils@gnu.org>.
.SH PRAWA AUTORSKIE
Copyright \(co 2002 Free Software Foundation, Inc.
.br
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
.SH "ZOBACZ TAK¯E"
Pe³na dokumentacja programu
.B stat
jest utrzymywana w postaci podrêcznika texinfo. Je¿eli programy
.B info 
i
.B stat
zosta³y poprawnie zainstalowane, to za pomoc± polecenia
.IP
.B info stat
.PP
mo¿na uzyskaæ dostêp do pe³nej wersji podrêcznika.
