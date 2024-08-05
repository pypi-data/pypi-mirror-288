# This file is part of CruscoPoetry.
# 
# CruscoPoetry is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# CruscoPoetry is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with CruscoPoetry. If not, see <http://www.gnu.org/licenses/>.

from cruscopoetry.syllabifiers import abstract
import re
from mum import Singleton
from .syllable import *


class WolofPhonemesParser(abstract.AbstractTokenizer):

	def __init__(self):

		#sets needed for syllabification
		self.long_vowels = ('à', 'aa', 'ee', 'ée', 'ii', 'oo', 'óo', 'uu')
		self.short_vowels = ('a', 'ë', 'e', 'é', 'i', 'o', 'ó', 'u', 'ə')
		
		self.vowels = self.long_vowels + self.short_vowels
		
		self.prenasalized_consonants = ('mb', 'nd', 'ng', 'nj')
		self.simple_consonants = ('b', 'c', 'd', 'f', 'g', 'j', 'k', 'l', 'm', 'n', 'ñ', 'ŋ', 'p', 'q', 'r', 's', 't', 'w', 'x', 'y')
		
		self.consonants = self.prenasalized_consonants + self.simple_consonants
					
		super().__init__(self.consonants, self.vowels)		
	
	def tokenize(self, wordstring: str):
		"""This function tokenizes the word in their phonemes. Characters that are not recognized as Wolof phonemes or are not a crasis marker will be ignored."""
		phonemes = list(super().tokenize(wordstring))
		
		#now we add the 'ə' vowel when it is prosodically necessary: that is, after prenasalized consonants and cluster of two consonants that are in word-final position or are followed by another 
		#consonant.
		#first we handle the prenasalized consonants before another consonant:
		for i in range(len(phonemes)-1):
			if (phonemes[i] in self.prenasalized_consonants and (phonemes[i+1] in self.consonants or phonemes[i+1] == abstract.Markers.CRASIS)):
				phonemes.insert(i+1, 'ə')

		#now we handle the cluster of two consonants before another consonant:
		for i in range(1, len(phonemes)-1):
			if (phonemes[i-1] in self.consonants and phonemes[i] in self.consonants and (phonemes[i+1] in self.consonants or phonemes[i+1] == abstract.Markers.CRASIS)):
				phonemes.insert(i+1, 'ə')
				
		#now we handle the prenasalized and cluster of two consonants in final position:
			if ((phonemes[-1] in self.consonants and phonemes[-2] in self.consonants) or (phonemes[-1] in self.prenasalized_consonants)):
				phonemes.append('ə')
		
		#where instead a crasis sign is present, we merge it and the two elements next to it (which should be two vowels) in one item.
		#We are sure that the crasis sign is not next to a word boundary because this has already been checked by the Cruscopoetry parser.
		#we must also consider crasis cases such as and_ak where the ə must be added before the crasis marker _. In this case, we first add a 'ə' phoneme after the consonant and then merge
		#it with the following vowel.
		#also when a simple consonant is present before the crasis (es. doom_i Aadam), we add a schwa after it.
		
		for i in range(len(phonemes)-1, -1, -1):
			if phonemes[i] == "_":
				#first case: crasis between two vowels (es. o_a)
				if phonemes[i-1] in self.vowels:
					phonemes[i-1] += phonemes[i] + phonemes[i+1]
					phonemes.pop(i)
					phonemes.pop(i)
				#second case: crasis between a simple consonant and a vowel (es. and_ak):
				else:
					phonemes[i] = "ə_" + phonemes[i+1]#we set phonemes[i] from '_' to 'ə_' + phonemes[i+1]
					phonemes.pop(i+1)#we remove the vowel after 
		
		return tuple(phonemes)
			

class WolofSyllabifier(abstract.AbstractSyllabifier):
	"""Syllabificator for wolof words. Implements the AbstractSyllabificator class from Cruscopoetry module."""
	
	def __init__(self):
		self.phonemes_parser = WolofPhonemesParser()
		
	def get_phonemes(self, wordstring: str):
		tokens = self.phonemes_parser.tokenize(wordstring)
		phonemes = []
		for token in tokens:
			if token in self.phonemes_parser.consonants:
				phonemes.append(Consonant(token))
			else:
				phonemes.append(Vowel(token))
		return tuple(phonemes)

	def auto_syllabify(self, word):
		"""Takes a string representing a Wolof word, syllabifies it according to Wolof syllabification rules, and stores the result in ``word.syllables`` as a sequence of :class:`WolofSyllable` instances."""

		#in case there is a hyphen in the word, we split it and call the function recursively:
		syllables = []
		if "-" in word:
			sections = [section for section in word.split("-") if section != ''] #the if condition prevents the formation of empty strings if a space was accidentally next to the hyphen
			for section in sections:
				section_syllables = self.auto_syllabify(section)
				syllables.extend(section_syllables)

		#otherwise, we properly syllabify it:
		else:
			syllables.append([])#a first list item for the first syllable
			phonemes = self.get_phonemes(word)
			
			i = 0
			while i < len(phonemes):

				#se il fonema è una consonante, lo appendiamo:
				if phonemes[i].is_vowel == False:
					syllables[-1].append(phonemes[i])

				#se il fonema è una vocale, appendiamo lui, eventualmente la consonante successiva e poi appendiamo una nuova lista in syllables:
				else:
					syllables[-1].append(phonemes[i])

					#first case: the phoneme is not the last or second last of the word
					if i+2 < len(phonemes):
						if phonemes[i+2].is_vowel == False:
							syllables[-1].append(phonemes[i+1])
							i+=1
						syllables.append([])

					#second_case: the phoneme is the last or second last of the word. If it is the last, we are done; if it is the penultimate, the last must be a consonant and therefore is part
					#of the same syllable. Therefore, we just extend syllable[-1] with all the phonemes after from phonemes[i]. Then we can break the loop:
					else:
						syllables[-1].extend(phonemes[i+1:])
						break

				i+=1

			#finally, we create the syllable objects return them:
			syllables = tuple(WolofSyllable(syllable).json_dict for syllable in syllables)
		return syllables
							
	def manually_syllabify(self, word: str):
		"""Same as :method:`syllabify`, but with manually syllabified words."""

		#first, we remove the square brackets:
		word = word[1:-1]
		
		#then we split on the pipe character:
		syllables = word.split("|")
		
		#then we get the phonemes objects from inside any item of syllables:
		syllables = [list(self.get_phonemes(syllable)) for syllable in syllables]
		#maybe in some cases the epenthetic vowel has not been added in the manual syllabification (for example, one writes [lep|p] instead of [lep|pə]). If so, we add it now:
		for syllable in syllables:
			if (len(syllable) == 1 and syllable[0].is_vowel == False):
				syllable.append(Vowel.epenthetic_schwa())
		
		#finally we create the WolofSyllable objects:
		
		syllables = tuple(WolofSyllable(syllable).json_dict for syllable in syllables)
		
		return syllables
		
		
