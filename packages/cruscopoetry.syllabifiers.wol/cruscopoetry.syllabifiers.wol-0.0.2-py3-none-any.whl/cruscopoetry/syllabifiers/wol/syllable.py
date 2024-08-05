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


class Phoneme(abstract.AbstractPhoneme):

	NULL_INSTANCE = None
	
	def __init__(self, phoneme):
		super().__init__(phoneme)

	@property
	def string(self):
		return super().string
	
	@property
	def is_null(self):
		return self == self.__class__.NULL_INSTANCE
		
	def __repr__(self):
		return "%s(%s)"%(self.__class__.__name__, self.string)
		
	@property
	def json_dict(self):
		if not self.is_null:
			return super().json_dict
		else:
			return {"base": ''}
		
	@classmethod
	def null(cls):
		"""Returns a null phoneme, which will be used when syllables lack onsets or cauda"""
		if cls.NULL_INSTANCE == None:
			cls.NULL_INSTANCE = cls(None)
		return cls.NULL_INSTANCE


class Consonant(abstract.AbstractConsonant, Phoneme):

	def __init__(self, phoneme):
		super().__init__(phoneme)
		self.is_vowel = False
		
	@property
	def json_dict(self):
		return super().json_dict


class CrasisError(Exception):

	def __init__(self, vowel1, vowel2):
		super().__init__()
		self.vowel1 = vowel1
		self.vowel2 = vowel2
	
	def __str__(self):
		return "Unrecognized crasis: %s_%s"%(self.vowel1, self.vowel2)


class Vowel(abstract.AbstractVowel, Phoneme):

	_CRASIS_DICT = {
		("à", "a"): "à", 
		("a", "à"): "à", 
		("a", "a"): "aa", 
		("aa", "a"): "aa", 
		("a", "aa"): "aa", 
		("a", "e"): "ee", 
		("a", "é"): "ee", 
		("aa", "e"): "ee", 
		("aa", "é"): "ee", 
		("a", "ee"): "ee", 
		("a", "ée"): "ee", 
		("a", "i"): "ee", 
		("aa", "i"): "ee", 
		("a", "ii"): "ee", 
		("aa", "ii"): "ee", 
		("a", "o"): "oo", 
		("aa", "o"): "oo", 
		("a", "oo"): "oo", 
		("aa", "oo"): "oo", 
		("a", "ó"): "oo", 
		("aa", "ó"): "oo", 
		("a", "óo"): "oo", 
		("aa", "óo"): "oo", 
		("a", "u"): "oo", 
		("aa", "u"): "oo", 
		("a", "uu"): "oo", 
		("aa", "uu"): "oo",
		("e", "a"): "ee", 
		("i", "a"): "ee", 
		("o", "a"): "oo", 
		("oo", "a"): "oo", 
		("o", "aa"): "oo", 
		("oo", "aa"): "oo", 
		("ó", "a"): "oo", 
		("óo", "a"): "oo", 
		("ó", "aa"): "oo", 
		("óo", "aa"): "oo", 
		("ə", "a"): "a", 
		("ə", "e"): "e", 
		("ə", "é"): "é", 
		("ə", "i"): "i", 
		("ə", "o"): "o", 
		("ə", "ó"): "ó", 
		("ə", "u"): "u", 
		("ə", "ë"): "ë", 
	}

	def __init__(self, phoneme):
		super().__init__(phoneme)
		self.is_vowel = True
		if self.is_from_crasis:
			self.value = self._get_crasis(self._base, self.crasis_vowel)
		else:
			self.value = self._base

	@classmethod
	def epenthetic_schwa(cls):
		return Vowel('ə')
		
	@property
	def string(self):
		return self.value

	@property
	def morae(self):
		#since short vowels in Wolof are always written with one character and long ones with two, this is simple:
		return len(self.value)
	
	def _get_crasis(self, vowel, crasis_vowel):
		key = (vowel, crasis_vowel)
		if key in self.__class__._CRASIS_DICT.keys():
			return self.__class__._CRASIS_DICT[key]
		else:
			raise CrasisError(vowel, crasis_vowel)
		
	@property
	def json_dict(self):
		return super().json_dict


class WolofSyllable(abstract.AbstractSyllable):

	def __init__(self, phonemes_list: list):
		#if phonemes_list has just one element it must be the nucleum: then, we add None before and after it, to mark the absence of consonants:
		if len(phonemes_list) == 1:
			phonemes_list.insert(0, Phoneme.null())
			phonemes_list.append(Phoneme.null())

		#if len(phonemes_list) == 2, either the nucleum (in word-initial position) or the cauda is absent and we substitute them with None values:
		if len(phonemes_list) == 2:
			if phonemes_list[0].is_vowel: #first item is vowel, therefore is the syllabic onset that lacks:
				phonemes_list.insert(0, Phoneme.null())
			else: #first item is consonant, therefore the second one is vowel and consequently it is the syllabic cauda that lacks:
				phonemes_list.append(Phoneme.null())
		
		#now we store the items of syltuple in these three attributes of the instance:
		self.onset, self.nucleum, self.cauda = phonemes_list
		
		#now we calculate the moraic length of the syllable. Attention! In Wolof syllables arrive up to three morae, and this must be taken into consideration in Khalilian metres.
		self.morae = self.nucleum.morae
		if not self.cauda.is_null:
			self.morae += 1

	def iter_phonemes(self):
		if not self.onset.is_null:
			yield self.onset
		yield self.nucleum
		if not self.cauda.is_null:
			yield self.cauda

	@property
	def stress(self):
		return self.nucleum.stress
	
	@stress.setter
	def stress(self, value):
		self.nucleum.stress = value % 7
	
	@property
	def as_string(self):
		ret_str = ""
		if not self.onset.is_null:
			ret_str += self.onset.string
		ret_str += self.nucleum.value
		if not self.cauda.is_null:
			ret_str += self.cauda.string
		return ret_str

	@property
	def json_dict(self) -> dict:
		#we organize in this dict also the data relative to the nucleum. But with morae we will return the syllabic length, rather than the one of the vowel.
		ret_dict = super().json_dict
		ret_dict.update({
			"morae": self.morae,
			"crasis": self.nucleum.string if self.nucleum.is_from_crasis else None,
			"string": self.as_string
		})
		return ret_dict
