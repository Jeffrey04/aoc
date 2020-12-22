module Main where

import Data.Char
import Debug.Trace (trace)
import MyLib (findAnswerPair, findAnswerTriplet)
import Text.Printf (printf)

main :: IO ()
main = do
  content <- getContents
  let list = getList content
   in printResult (list >>= findAnswerPair) (list >>= findAnswerTriplet)
  where
    getList :: String -> Maybe [Int]
    getList content = return $ read <$> lines content

    printResult :: Maybe Int -> Maybe Integer -> IO ()
    printResult Nothing _ = error "Bad pair"
    printResult _ Nothing = error "Bad triplet"
    printResult (Just pair) (Just triplet) = printf "HASKELL:\t%d\t%d\n" pair triplet
