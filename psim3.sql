-- phpMyAdmin SQL Dump
-- version 4.6.5.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Czas generowania: 22 Kwi 2017, 15:42
-- Wersja serwera: 10.1.21-MariaDB
-- Wersja PHP: 5.6.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Baza danych: `psim`
--

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `grupy`
--

CREATE TABLE `grupy` (
  `ID_grupy` int(8) NOT NULL,
  `Nazwa_grupy` varchar(50) COLLATE utf8_polish_ci NOT NULL,
  `ID_zalozyciela` int(8) NOT NULL,
  `ID_zainteresowania` int(8) NOT NULL,
  `Termin` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `kontakty`
--

CREATE TABLE `kontakty` (
  `ID_uzytkownika` int(11) NOT NULL,
  `ID_kontaktu` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `lokalizacje`
--

CREATE TABLE `lokalizacje` (
  `ID_lokalizacji` int(8) NOT NULL,
  `X` int(4) NOT NULL,
  `Y` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `sklad_grupy`
--

CREATE TABLE `sklad_grupy` (
  `ID_grupy` int(8) NOT NULL,
  `ID_uzytkownika` int(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `terminy`
--

CREATE TABLE `terminy` (
  `ID_terminu` int(8) NOT NULL,
  `ID_grupy` int(8) NOT NULL,
  `ID_uzytkownika` int(8) NOT NULL,
  `Termin` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `użytkownicy`
--

CREATE TABLE `użytkownicy` (
  `ID_uzytkownika` int(8) NOT NULL,
  `Imie` varchar(50) COLLATE utf8_polish_ci NOT NULL,
  `Nazwisko` varchar(50) COLLATE utf8_polish_ci NOT NULL,
  `Mail` varchar(25) COLLATE utf8_polish_ci NOT NULL,
  `Login` varchar(16) COLLATE utf8_polish_ci NOT NULL,
  `Haslo` varchar(25) COLLATE utf8_polish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `wydarzenia`
--

CREATE TABLE `wydarzenia` (
  `ID_wydarzenia` int(8) NOT NULL,
  `Nazwa_wydarzenia` varchar(50) COLLATE utf8_polish_ci NOT NULL,
  `ID_lokalizacji` int(8) NOT NULL,
  `Termin` datetime NOT NULL,
  `ID_zainteresowania` int(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `zainteresowania`
--

CREATE TABLE `zainteresowania` (
  `ID_zainteresowania` int(8) NOT NULL,
  `Nazwa_zainteresowania` varchar(50) COLLATE utf8_polish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;

--
-- Indeksy dla zrzutów tabel
--

--
-- Indexes for table `grupy`
--
ALTER TABLE `grupy`
  ADD PRIMARY KEY (`ID_grupy`),
  ADD KEY `ID_zalozyciela` (`ID_zalozyciela`),
  ADD KEY `ID_zainteresowania` (`ID_zainteresowania`);

--
-- Indexes for table `kontakty`
--
ALTER TABLE `kontakty`
  ADD PRIMARY KEY (`ID_uzytkownika`,`ID_kontaktu`),
  ADD KEY `ID_kontaktu` (`ID_kontaktu`);

--
-- Indexes for table `lokalizacje`
--
ALTER TABLE `lokalizacje`
  ADD PRIMARY KEY (`ID_lokalizacji`);

--
-- Indexes for table `sklad_grupy`
--
ALTER TABLE `sklad_grupy`
  ADD PRIMARY KEY (`ID_grupy`,`ID_uzytkownika`),
  ADD KEY `ID_uzytkownik` (`ID_uzytkownika`);

--
-- Indexes for table `terminy`
--
ALTER TABLE `terminy`
  ADD PRIMARY KEY (`ID_terminu`),
  ADD KEY `ID_grup` (`ID_grupy`),
  ADD KEY `ID_uzytk` (`ID_uzytkownika`);

--
-- Indexes for table `użytkownicy`
--
ALTER TABLE `użytkownicy`
  ADD PRIMARY KEY (`ID_uzytkownika`);

--
-- Indexes for table `wydarzenia`
--
ALTER TABLE `wydarzenia`
  ADD PRIMARY KEY (`ID_wydarzenia`),
  ADD KEY `ID_lokalizacji` (`ID_lokalizacji`),
  ADD KEY `ID_zainteresowani` (`ID_zainteresowania`);

--
-- Indexes for table `zainteresowania`
--
ALTER TABLE `zainteresowania`
  ADD PRIMARY KEY (`ID_zainteresowania`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT dla tabeli `grupy`
--
ALTER TABLE `grupy`
  MODIFY `ID_grupy` int(8) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT dla tabeli `lokalizacje`
--
ALTER TABLE `lokalizacje`
  MODIFY `ID_lokalizacji` int(8) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT dla tabeli `terminy`
--
ALTER TABLE `terminy`
  MODIFY `ID_terminu` int(8) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT dla tabeli `użytkownicy`
--
ALTER TABLE `użytkownicy`
  MODIFY `ID_uzytkownika` int(8) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT dla tabeli `wydarzenia`
--
ALTER TABLE `wydarzenia`
  MODIFY `ID_wydarzenia` int(8) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT dla tabeli `zainteresowania`
--
ALTER TABLE `zainteresowania`
  MODIFY `ID_zainteresowania` int(8) NOT NULL AUTO_INCREMENT;
--
-- Ograniczenia dla zrzutów tabel
--

--
-- Ograniczenia dla tabeli `grupy`
--
ALTER TABLE `grupy`
  ADD CONSTRAINT `ID_zainteresowania` FOREIGN KEY (`ID_zainteresowania`) REFERENCES `zainteresowania` (`ID_zainteresowania`),
  ADD CONSTRAINT `ID_zalozyciela` FOREIGN KEY (`ID_zalozyciela`) REFERENCES `użytkownicy` (`ID_uzytkownika`);

--
-- Ograniczenia dla tabeli `kontakty`
--
ALTER TABLE `kontakty`
  ADD CONSTRAINT `ID_kontaktu` FOREIGN KEY (`ID_kontaktu`) REFERENCES `użytkownicy` (`ID_uzytkownika`),
  ADD CONSTRAINT `ID_uzytkownika` FOREIGN KEY (`ID_uzytkownika`) REFERENCES `użytkownicy` (`ID_uzytkownika`);

--
-- Ograniczenia dla tabeli `sklad_grupy`
--
ALTER TABLE `sklad_grupy`
  ADD CONSTRAINT `ID_grupy` FOREIGN KEY (`ID_grupy`) REFERENCES `grupy` (`ID_grupy`),
  ADD CONSTRAINT `ID_uzytkownik` FOREIGN KEY (`ID_uzytkownika`) REFERENCES `użytkownicy` (`ID_uzytkownika`);

--
-- Ograniczenia dla tabeli `terminy`
--
ALTER TABLE `terminy`
  ADD CONSTRAINT `ID_grup` FOREIGN KEY (`ID_grupy`) REFERENCES `grupy` (`ID_grupy`),
  ADD CONSTRAINT `ID_uzytk` FOREIGN KEY (`ID_uzytkownika`) REFERENCES `użytkownicy` (`ID_uzytkownika`);

--
-- Ograniczenia dla tabeli `wydarzenia`
--
ALTER TABLE `wydarzenia`
  ADD CONSTRAINT `ID_lokalizacji` FOREIGN KEY (`ID_lokalizacji`) REFERENCES `lokalizacje` (`ID_lokalizacji`),
  ADD CONSTRAINT `ID_zainteresowani` FOREIGN KEY (`ID_zainteresowania`) REFERENCES `zainteresowania` (`ID_zainteresowania`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
