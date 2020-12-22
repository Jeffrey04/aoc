module Main (main) where

import MyLib (findAnswerPair, findAnswerTriplet)
import Test.Hspec

main :: IO ()
main = hspec $ do
  describe "Prelude.head" $ do
    it "Pair test" $ do
      findAnswerPair [1721, 979, 366, 299, 675, 1456] `shouldBe` Just (514579 :: Int)

    it "Triplet test" $ do
      findAnswerTriplet [1721, 979, 366, 299, 675, 1456] `shouldBe` Just (241861950 :: Integer)