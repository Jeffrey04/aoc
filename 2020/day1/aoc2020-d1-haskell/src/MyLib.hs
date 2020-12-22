module MyLib (findAnswerPair, findAnswerTriplet) where

findSumPair :: Int -> [Int] -> Maybe (Int, Int)
findSumPair _ [] = Nothing
findSumPair _ [_] = Nothing
findSumPair target (x : xs) = go (Just x) xs (target - x)
  where
    go :: Maybe Int -> [Int] -> Int -> Maybe (Int, Int)
    go _ [] _ = findSumPair target xs
    go (Just fst) (y : ys) residual
      | y == residual = Just (fst, y)
      | otherwise = go (Just fst) ys residual

findSumTriplet :: Int -> [Int] -> Maybe (Int, Int, Int)
findSumTriplet _ [] = Nothing
findSumTriplet _ [_] = Nothing
findSumTriplet _ [_, _] = Nothing
findSumTriplet target (x : xs) = goFst target (Just x) xs
  where
    goFst :: Int -> Maybe Int -> [Int] -> Maybe (Int, Int, Int)
    goFst _ _ [] = Nothing
    goFst residual (Just first) (y : ys) = case goSnd (residual - first) (Just y) ys of
      Just (second, third) -> Just (first, second, third)
      Nothing -> goFst residual (Just y) ys

    goSnd :: Int -> Maybe Int -> [Int] -> Maybe (Int, Int)
    goSnd _ _ [] = Nothing
    goSnd residual (Just second) (y : ys) = case goTrd (residual - second) (Just y) ys of
      Just third -> Just (second, third)
      Nothing -> goSnd residual (Just y) ys

    goTrd :: Int -> Maybe Int -> [Int] -> Maybe Int
    goTrd _ _ [] = Nothing
    goTrd residual (Just third) (y : ys)
      | residual == third = Just third
      | otherwise = goTrd residual (Just y) ys

findAnswerPair :: [Int] -> Maybe Int
findAnswerPair x = do
  pair <- findSumPair 2020 x
  return $ uncurry (*) pair

findAnswerTriplet :: [Int] -> Maybe Integer
findAnswerTriplet x = do
  (first, second, third) <- findSumTriplet 2020 x
  return $ product (toInteger <$> [first, second, third])