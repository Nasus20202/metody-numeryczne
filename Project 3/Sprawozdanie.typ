#set text(
  font: "New Computer Modern",
  size: 12pt
)
#set page(paper: "a4", margin: (x: 1cm, y: 1cm), numbering: "1")
#set heading(numbering: "1.")
#set figure(supplement: none)
#set grid(columns: 2, gutter: 2mm,)
#set pad(x: -0.8cm)

#let files = ("chelm.txt", "in_mountain.data", "tczew_starogard.txt", "ulm_lugano.txt")
#let sizes = (6, 11, 16, 26, 52, 103)


#align(center)[
  #stack(
    v(12pt),
    text(size: 20pt)[Metody numeryczne - Aproksymacja profilu wysokościowego],
    v(12pt),
    text(size: 15pt)[Krzysztof Nasuta, s193328],
    v(8pt),
    text(size: 12pt)[#datetime.today().display("[day]-[month]-[year]")]
  )
]


#outline(title: "Spis treści")


= Wstęp

Celem projektu było zaimplementowanie dwóch metod interpolacji funkcji: metody Lagrange'a oraz metody funkcji sklejanych. Następnie należało wykorzystać te metody do interpolacji profilu wysokościowego. W projekcie przeprowadzono testy dla czterech różnych zbiorów danych, a wyniki przedstawiono w postaci wykresów. W projekcie porównano również wpływ ilości węzłów na jakość interpolacji, oraz rozmieszczenia węzłów w przypadku metody Lagrange'a.


Do implementacji wykorzystano język Python wraz z biblioteką `matplotlib` do generowania wykresów.


= Opis metod

== Metoda Lagrange'a dla równoodległych węzłów


Metoda Lagrange'a pozwala na obliczenie wielomianu stopnia `n` na podstawie `n+1` węzłów. Jest to jedna z najprostszych metod interpolacji. Wynik interpolacji Lagrange'a jest taki sam jak wynik metody Vandermonde'a. Jej zaletą jest brak konieczności rozwiązywania układu równań, stabilność numeryczna oraz prostota implementacji.


Bazą dla metody Lagrange'a jest wzór:
$ phi.alt_i (x) = limits(product)_(j=1,j!=i)^(n+1) frac((x - x_j), (x_i - x_j)) $


Następnie wielomian interpolacyjny Lagrange'a można zapisać jako:
$ F(x) = sum_(i=1)^(n+1) y_i phi.alt_i (x) $


Pomimo swoich zalet, metoda Lagrange'a ma również wady. Jedną z nich jest podatność na efekt Rungego, czyli oscylacje wielomianu interpolacyjnego w okolicach krańców przedziału. W celu zminimalizowania tego efektu można zastosować interpolację w węzłach Czebyszewa. W projekcie porównano jakość interpolacji z ich zastosowaniem w stosunku do równoodległych węzłów. Węzły Czebyszewa w przedziale $[a, b]$ można obliczyć ze wzoru:
$ x_k = frac(a + b, 2) + frac(b - a, 2) cos(frac(2k - 1, 2k) pi), k = 1, ..., n $


== Metoda funkcji sklejanych


Metoda funkcji sklejanych polega na wyznaczeniu wielomianu stałego stopnia na każdym z przedziałów między węzłami. Wielomiany te są tak dobrane, aby były ciągłe oraz miały ciągłe pochodne pierwszego i drugiego rzędu. W projekcie zaimplemetnowano interpolację funkcjami sklejanymi stopnia 3. Wielomiany te są zdefiniowane jako:
$ S_i (x) = a_i + b_i (x - x_i) + c_i (x - x_i)^2 + d_i (x - x_i)^3 $


Metoda funkcji sklejanych pozwala na wyznaczenie współczynników $a_i, b_i, c_i, d_i$ dla każdego z przedziałów poprzez rozwiązanie układu równań. W projekcie do rozwiązania układu równań wykorzystano faktoryzację LU. Metoda funkcji sklejanych jest bardziej skomplikowana niż metoda Lagrange'a, ale pozwala na uzyskanie lepszych wyników. Jest też odporna na efekt Rungego.


Układ równań do rozwiązania dla metody funkcji sklejanych można zapisać jako:
$ S_i (x_i) = y_i, i = 0, ..., n-1 & "Wartość funkcji w węzłach" $
$ S_i (x_(i+1)) = y_(i+1), i = 0, ..., n-1 & "Ciągłość funkcji w węzłach" $
$ S''_0(x_0) = 0 & "Zerowanie drugiej pochodnej w punkcie początkowym" $
$ S''_(n-1)(x_n) = 0 & "Zerowanie drugiej pochodnej w punkcie końcowym" $
$ S'_i (x_i) = S'_(i-1)(x_i), i = 1, ..., n-1 & "Zerowanie pierwszej pochodnej w punktach" $
$ S''_i (x_i) = S''_(i-1)(x_i), i = 1, ..., n-1 & "Zerowanie drugiej pochodnej w punktach" $


= Dane wejściowe


W projekcie przeprowadzono testy dla czterech różnych zbiorów danych. Wszystkie zbiory danych zawierają 512 punktów. 
- `chelm.txt` - dane o małej zmienności wysokości
- `in_mountain.data` - dane o początkowym wzroście wysokości, długim odcinku płaskim oraz końcowym spadku
- `tczew_starogard.txt` - dane o wzroście wysokości z dużymi oscylacjami miejscowymi
- `ulm_lugano.txt` - dane o bardzo dużej zmienności wysokości i dużych oscylacjach miejscowych

Poniżej przedstawiono wykresy dla każdego z nich.

#pad(
  grid(
    ..files.map(file => figure(image("plots/" + file + "/input_data.png"), caption: [Dane wejściowe dla pliku #file]))
  )
)


= Wyniki interpolacji metodą Lagrange'a dla równoodległych węzłów


Dla każdego zbioru danych przeprowadzono interpolację metodą Lagrange'a dla 6, 11, 16, 26, 52 oraz 103 węzłów wejściowych. Wartości wybranych węzłów są rozmieszczone równomiernie. Liczba węzłów została dobrana tak, aby umożliwić wybranie z 512 punktów węzłów równoodległych.


Za pomocą interpolacji Lagrange'a obliczono wartości funkcji w 512 punktach. Poniżej przedstawiono wykresy interpolacji dla każdego zbioru danych.


#for file in files{
  [== Interpolacja Lagrange'a - #file]
  pad(
    grid(
      ..sizes.map(size => figure(image("plots/" + file + "/lagrange_" + str(size) + "_points.png"), caption: text([#size węzłów], size: 7pt)))
    )
  )
}


== Podsumowanie interpolacji metodą Lagrange'a dla równoodległych węzłów


Jak można zauważyć, wyniki interpolacji metodą Lagrange'a nie spełniają oczekiwań. W przypadku małej ilości węzłów, czyli 6 oraz 11, wyniki są mało dokładne, ale efekt Rungego nie jest widoczny. Wraz ze wzrostem ilości węzłów, wyniki interpolacji pogarszają się. Widać wyraźnie efekt Rungego, czyli oscylacje wielomianu interpolacyjnego w okolicach krańców przedziału. Już przy 26 węzłach wynik interpolacji jest bardzo zaburzony.


= Wyniki interpolacji metodą Lagrange'a dla węzłów Czebyszewa


W celu zminimalizowania efektu Rungego zastosowano interpolację metodą Lagrange'a dla węzłów Czebyszewa. Z racji tego, że nie znamy danych wejściowych, nie jesteśmy w stanie idealnie dobrać węzłów Czebyszewa. W projekcie wybrano z węzłów wejściowych bez powtórzeń te, które są najbliżej węzłów Czebyszewa.


#for file in files{
  [== Interpolacja Lagrange'a (węzły Czebyszewa) - #file]
  pad(
    grid(
      ..sizes.map(size => figure(image("plots/" + file + "/lagrange_" + str(size) + "_points_chebyshev.png"), caption: text([#size węzłów], size: 7pt)))
    )
  )
}


== Podsumowanie interpolacji metodą Lagrange'a dla węzłów Czebyszewa


Jak można wywnioskować z powyższych wykresów, interpolacja metodą Lagrange'a dla węzłów Czebyszewa jest bardziej stabilna niż dla równoodległych węzłów. Dla wszystkich danych udało się uzyskać dobre wyniki interpolacji. Efekt Rungego jest praktycznie niewidoczny. Nawet dla 103 węzłów interpolacja jest bardzo dokładna.


Warto zauważyć, że w przypadku danych wejściowych z 512 punktów, wybór węzłów Czebyszewa był możliwy. W praktyce, dla mniejszej ilości danych, dobór węzłów Czebyszewa może być trudny. Wymaga on wybrania nierównomiernie rozmieszczonych węzłów, co jest trudne do osiągnięcia.


= Wyniki interpolacji metodą funkcji sklejanych


Dla każdego zbioru danych przeprowadzono interpolację metodą funkcji sklejanych. W projekcie zaimplementowano interpolację funkcjami sklejanymi stopnia 3. Również dla tej metody wybrano odpowiednio 6, 11, 16, 26, 52 oraz 103 węzłów wejściowych. Wartości wybranych węzłów są rozmieszczone równomiernie. Na ich podstawie obliczono wartości funkcji w 512 punktach. Poniżej przedstawiono wykresy interpolacji dla każdego zbioru danych.


#for file in files{
  [== Interpolacja funkcjami sklejanymi - #file]
  pad(
    grid(
      ..sizes.map(size => figure(image("plots/" + file + "/spline_" + str(size) + "_points.png"), caption: text([#size węzłów], size: 7pt)))
    )
  )
}


== Podsumowanie interpolacji metodą funkcji sklejanych


Interpolacja metodą funkcji sklejanych pozwala na uzyskanie bardzo dokładnych wyników. Nawet przy 11 węzłach wejściowych wynik interpolacji przypomina oryginalną funkcję. Dla 52 czy 103 węzłów interpolacja jest bardzo dokładna. Jak również możemy zauważyć, metoda funkcji sklejanych jest odporna na efekt Rungego. Pozwala to na zwiększenie ilości węzłów bez obaw o pogorszenie wyników. Warto zauważyć, że metoda funkcji sklejanych, w przeciwieństwie do metody Lagrange'a, spełnia swoje zadanie dla danych równomiernie rozmieszczonych.


= Podsumowanie


W uzyskanych wyników interpolacji można zauważyć, że metoda Lagrange'a dla węzłów równoodległych nie jest odpowiednia do interpolacji profilu wysokościowego. Dla małej ilości węzłów wejściowych wyniki są mało dokładne, a po ich zwiększeniu pojawia się efekt Rungego. Zastosowanie węzłów Czebyszewa pozwala na zminimalizowanie tego efektu, ale nie jest to rozwiązanie idealne. Wymaga ono wyboru nierównomiernie rozmieszczonych węzłów, co jest trudne do osiągnięcia w praktyce. W plikach z danymi wejściowymi znajdowało się aż 512 punktów, co pozwalało na dobre dobranie węzłów Czebyszewa. W przypadku mniejszej ilości danych, nie byłoby to możliwe. Z tego powodu metoda Lagrange'a nie jest odpowiednia do interpolacji profilu wysokościowego.


Metoda funkcji sklejanych pozwala na uzyskanie bardzo dokładnych wyników interpolacji. Jest ona odporna na efekt Rungego, co pozwala na zwiększanie ilości węzłów bez obaw o pogorszenie wyników. Metoda funkcji sklejanych spełnia swoje zadanie dla danych równomiernie rozmieszczonych, co jest idealne w przypadku profilu wysokościowego.


Podsumowując, pomimo większej trudności implementacyjnej, metoda funkcji sklejanych jest bardziej odpowiednia do interpolacji profilu wysokościowego niż metoda Lagrange'a. Pozwala ona na uzyskanie dokładnych wyników nawet dla małej ilości węzłów wejściowych. Możemy poprawić jakość interpolacji poprzez zwiększenie ilości węzłów, co nie wpłynie negatywnie na wyniki. Metoda funkcji sklejanych jest również bardziej odporna na efekt Rungego, co pozwala na uzyskanie dokładnych wyników bez obaw o zaburzenia.

