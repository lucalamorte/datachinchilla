/* ============================================================
   problemas.js

   Lo genera build-problemas.py. No se edita a mano.

   La lista, el patrón y el link. El enunciado se lee en la
   plataforma de origen, que es de quien es; acá vive el orden
   y tu avance, que es lo que allá no queda.
   ============================================================ */
var PROBLEMAS = [
 {
  "id": "blind75",
  "nombre": "Blind 75",
  "lang": "Python",
  "fuente": "LeetCode",
  "url": "https://leetcode.com/problemset/",
  "d": "Los 75 que cubren los patrones que se repiten en las entrevistas de algoritmos.",
  "items": [
   {
    "n": 128,
    "t": "Longest Consecutive Sequence",
    "d": "medio",
    "ac": 47.2,
    "p": "Arrays y hashing",
    "u": "https://leetcode.com/problems/longest-consecutive-sequence/"
   },
   {
    "n": 1,
    "t": "Two Sum",
    "d": "facil",
    "ac": 58.1,
    "p": "Arrays y hashing",
    "u": "https://leetcode.com/problems/two-sum/"
   },
   {
    "n": 3,
    "t": "Longest Substring Without Repeating Characters",
    "d": "medio",
    "ac": 39.9,
    "p": "Ventana movil",
    "u": "https://leetcode.com/problems/longest-substring-without-repeating-characters/"
   },
   {
    "n": 5,
    "t": "Longest Palindromic Substring",
    "d": "medio",
    "ac": 38.6,
    "p": "Programacion dinamica",
    "u": "https://leetcode.com/problems/longest-palindromic-substring/"
   },
   {
    "n": 133,
    "t": "Clone Graph",
    "d": "medio",
    "ac": 66.1,
    "p": "Grafos",
    "u": "https://leetcode.com/problems/clone-graph/"
   },
   {
    "n": 261,
    "t": "Graph Valid Tree",
    "d": "medio",
    "ac": 50.1,
    "p": "Grafos",
    "u": "https://leetcode.com/problems/graph-valid-tree/"
   },
   {
    "n": 647,
    "t": "Palindromic Substrings",
    "d": "medio",
    "ac": 73.2,
    "p": "Programacion dinamica",
    "u": "https://leetcode.com/problems/palindromic-substrings/"
   },
   {
    "n": 11,
    "t": "Container With Most Water",
    "d": "medio",
    "ac": 60.8,
    "p": "Dos punteros",
    "u": "https://leetcode.com/problems/container-with-most-water/"
   },
   {
    "n": 139,
    "t": "Word Break",
    "d": "medio",
    "ac": 49.8,
    "p": "Programacion dinamica",
    "u": "https://leetcode.com/problems/word-break/"
   },
   {
    "n": 141,
    "t": "Linked List Cycle",
    "d": "facil",
    "ac": 55.0,
    "p": "Lista enlazada",
    "u": "https://leetcode.com/problems/linked-list-cycle/"
   },
   {
    "n": 268,
    "t": "Missing Number",
    "d": "facil",
    "ac": 72.6,
    "p": "Bits",
    "u": "https://leetcode.com/problems/missing-number/"
   },
   {
    "n": 15,
    "t": "3Sum",
    "d": "medio",
    "ac": 39.8,
    "p": "Dos punteros",
    "u": "https://leetcode.com/problems/3sum/"
   },
   {
    "n": 143,
    "t": "Reorder List",
    "d": "medio",
    "ac": 66.1,
    "p": "Lista enlazada",
    "u": "https://leetcode.com/problems/reorder-list/"
   },
   {
    "n": 269,
    "t": "Alien Dictionary",
    "d": "dificil",
    "ac": 37.3,
    "p": "Grafos",
    "u": "https://leetcode.com/problems/alien-dictionary/"
   },
   {
    "n": 271,
    "t": "Encode and Decode Strings",
    "d": "medio",
    "ac": 51.9,
    "p": "Arrays y hashing",
    "u": "https://leetcode.com/problems/encode-and-decode-strings/"
   },
   {
    "n": 19,
    "t": "Remove Nth Node From End of List",
    "d": "medio",
    "ac": 52.5,
    "p": "Lista enlazada",
    "u": "https://leetcode.com/problems/remove-nth-node-from-end-of-list/"
   },
   {
    "n": 20,
    "t": "Valid Parentheses",
    "d": "facil",
    "ac": 44.8,
    "p": "Pila",
    "u": "https://leetcode.com/problems/valid-parentheses/"
   },
   {
    "n": 21,
    "t": "Merge Two Sorted Lists",
    "d": "facil",
    "ac": 68.8,
    "p": "Lista enlazada",
    "u": "https://leetcode.com/problems/merge-two-sorted-lists/"
   },
   {
    "n": 23,
    "t": "Merge k Sorted Lists",
    "d": "dificil",
    "ac": 60.4,
    "p": "Lista enlazada",
    "u": "https://leetcode.com/problems/merge-k-sorted-lists/"
   },
   {
    "n": 152,
    "t": "Maximum Product Subarray",
    "d": "medio",
    "ac": 37.0,
    "p": "Programacion dinamica",
    "u": "https://leetcode.com/problems/maximum-product-subarray/"
   },
   {
    "n": 153,
    "t": "Find Minimum in Rotated Sorted Array",
    "d": "medio",
    "ac": 55.3,
    "p": "Busqueda binaria",
    "u": "https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/"
   },
   {
    "n": 33,
    "t": "Search in Rotated Sorted Array",
    "d": "medio",
    "ac": 45.6,
    "p": "Busqueda binaria",
    "u": "https://leetcode.com/problems/search-in-rotated-sorted-array/"
   },
   {
    "n": 417,
    "t": "Pacific Atlantic Water Flow",
    "d": "medio",
    "ac": 61.4,
    "p": "Grafos",
    "u": "https://leetcode.com/problems/pacific-atlantic-water-flow/"
   },
   {
    "n": 39,
    "t": "Combination Sum",
    "d": "medio",
    "ac": 77.1,
    "p": "Backtracking",
    "u": "https://leetcode.com/problems/combination-sum/"
   },
   {
    "n": 295,
    "t": "Find Median from Data Stream",
    "d": "dificil",
    "ac": 55.0,
    "p": "Monticulo",
    "u": "https://leetcode.com/problems/find-median-from-data-stream/"
   },
   {
    "n": 297,
    "t": "Serialize and Deserialize Binary Tree",
    "d": "dificil",
    "ac": 61.1,
    "p": "Arboles",
    "u": "https://leetcode.com/problems/serialize-and-deserialize-binary-tree/"
   },
   {
    "n": 424,
    "t": "Longest Repeating Character Replacement",
    "d": "medio",
    "ac": 60.6,
    "p": "Ventana movil",
    "u": "https://leetcode.com/problems/longest-repeating-character-replacement/"
   },
   {
    "n": 300,
    "t": "Longest Increasing Subsequence",
    "d": "medio",
    "ac": 59.9,
    "p": "Programacion dinamica",
    "u": "https://leetcode.com/problems/longest-increasing-subsequence/"
   },
   {
    "n": 48,
    "t": "Rotate Image",
    "d": "medio",
    "ac": 80.7,
    "p": "Matrices",
    "u": "https://leetcode.com/problems/rotate-image/"
   },
   {
    "n": 49,
    "t": "Group Anagrams",
    "d": "medio",
    "ac": 73.2,
    "p": "Arrays y hashing",
    "u": "https://leetcode.com/problems/group-anagrams/"
   },
   {
    "n": 435,
    "t": "Non-overlapping Intervals",
    "d": "medio",
    "ac": 57.7,
    "p": "Intervalos",
    "u": "https://leetcode.com/problems/nonoverlapping-intervals/"
   },
   {
    "n": 53,
    "t": "Maximum Subarray",
    "d": "medio",
    "ac": 53.8,
    "p": "Programacion dinamica",
    "u": "https://leetcode.com/problems/maximum-subarray/"
   },
   {
    "n": 54,
    "t": "Spiral Matrix",
    "d": "medio",
    "ac": 57.8,
    "p": "Matrices",
    "u": "https://leetcode.com/problems/spiral-matrix/"
   },
   {
    "n": 55,
    "t": "Jump Game",
    "d": "medio",
    "ac": 41.5,
    "p": "Codicioso",
    "u": "https://leetcode.com/problems/jump-game/"
   },
   {
    "n": 56,
    "t": "Merge Intervals",
    "d": "medio",
    "ac": 52.7,
    "p": "Intervalos",
    "u": "https://leetcode.com/problems/merge-intervals/"
   },
   {
    "n": 57,
    "t": "Insert Interval",
    "d": "medio",
    "ac": 45.9,
    "p": "Intervalos",
    "u": "https://leetcode.com/problems/insert-interval/"
   },
   {
    "n": 572,
    "t": "Subtree of Another Tree",
    "d": "facil",
    "ac": 52.1,
    "p": "Arboles",
    "u": "https://leetcode.com/problems/subtree-of-another-tree/"
   },
   {
    "n": 62,
    "t": "Unique Paths",
    "d": "medio",
    "ac": 67.2,
    "p": "Programacion dinamica",
    "u": "https://leetcode.com/problems/unique-paths/"
   },
   {
    "n": 190,
    "t": "Reverse Bits",
    "d": "facil",
    "ac": 69.3,
    "p": "Bits",
    "u": "https://leetcode.com/problems/reverse-bits/"
   },
   {
    "n": 191,
    "t": "Number of 1 Bits",
    "d": "facil",
    "ac": 77.5,
    "p": "Bits",
    "u": "https://leetcode.com/problems/number-of-1-bits/"
   },
   {
    "n": 322,
    "t": "Coin Change",
    "d": "medio",
    "ac": 49.1,
    "p": "Programacion dinamica",
    "u": "https://leetcode.com/problems/coin-change/"
   },
   {
    "n": 323,
    "t": "Number of Connected Components in an Undirected Graph",
    "d": "medio",
    "ac": 65.1,
    "p": "Grafos",
    "u": "https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/"
   },
   {
    "n": 70,
    "t": "Climbing Stairs",
    "d": "facil",
    "ac": 54.3,
    "p": "Programacion dinamica",
    "u": "https://leetcode.com/problems/climbing-stairs/"
   },
   {
    "n": 198,
    "t": "House Robber",
    "d": "medio",
    "ac": 53.6,
    "p": "Programacion dinamica",
    "u": "https://leetcode.com/problems/house-robber/"
   },
   {
    "n": 200,
    "t": "Number of Islands",
    "d": "medio",
    "ac": 65.1,
    "p": "Grafos",
    "u": "https://leetcode.com/problems/number-of-islands/"
   },
   {
    "n": 73,
    "t": "Set Matrix Zeroes",
    "d": "medio",
    "ac": 63.5,
    "p": "Matrices",
    "u": "https://leetcode.com/problems/set-matrix-zeroes/"
   },
   {
    "n": 76,
    "t": "Minimum Window Substring",
    "d": "dificil",
    "ac": 48.4,
    "p": "Ventana movil",
    "u": "https://leetcode.com/problems/minimum-window-substring/"
   },
   {
    "n": 206,
    "t": "Reverse Linked List",
    "d": "facil",
    "ac": 81.0,
    "p": "Lista enlazada",
    "u": "https://leetcode.com/problems/reverse-linked-list/"
   },
   {
    "n": 79,
    "t": "Word Search",
    "d": "medio",
    "ac": 48.1,
    "p": "Matrices",
    "u": "https://leetcode.com/problems/word-search/"
   },
   {
    "n": 207,
    "t": "Course Schedule",
    "d": "medio",
    "ac": 52.2,
    "p": "Grafos",
    "u": "https://leetcode.com/problems/course-schedule/"
   },
   {
    "n": 208,
    "t": "Implement Trie (Prefix Tree)",
    "d": "medio",
    "ac": 70.0,
    "p": "Trie",
    "u": "https://leetcode.com/problems/implement-trie-prefix-tree/"
   },
   {
    "n": 338,
    "t": "Counting Bits",
    "d": "facil",
    "ac": 80.8,
    "p": "Bits",
    "u": "https://leetcode.com/problems/counting-bits/"
   },
   {
    "n": 211,
    "t": "Design Add and Search Words Data Structure",
    "d": "medio",
    "ac": 49.0,
    "p": "Trie",
    "u": "https://leetcode.com/problems/design-add-and-search-words-data-structure/"
   },
   {
    "n": 212,
    "t": "Word Search II",
    "d": "dificil",
    "ac": 38.9,
    "p": "Trie",
    "u": "https://leetcode.com/problems/word-search-ii/"
   },
   {
    "n": 213,
    "t": "House Robber II",
    "d": "medio",
    "ac": 45.5,
    "p": "Programacion dinamica",
    "u": "https://leetcode.com/problems/house-robber-ii/"
   },
   {
    "n": 217,
    "t": "Contains Duplicate",
    "d": "facil",
    "ac": 64.7,
    "p": "Arrays y hashing",
    "u": "https://leetcode.com/problems/contains-duplicate/"
   },
   {
    "n": 91,
    "t": "Decode Ways",
    "d": "medio",
    "ac": 38.5,
    "p": "Programacion dinamica",
    "u": "https://leetcode.com/problems/decode-ways/"
   },
   {
    "n": 347,
    "t": "Top K Frequent Elements",
    "d": "medio",
    "ac": 67.3,
    "p": "Arrays y hashing",
    "u": "https://leetcode.com/problems/top-k-frequent-elements/"
   },
   {
    "n": 253,
    "t": "Meeting Rooms II",
    "d": "medio",
    "ac": 52.8,
    "p": "Intervalos",
    "u": "https://leetcode.com/problems/meeting-rooms-ii/"
   },
   {
    "n": 98,
    "t": "Validate Binary Search Tree",
    "d": "medio",
    "ac": 36.3,
    "p": "Arboles",
    "u": "https://leetcode.com/problems/validate-binary-search-tree/"
   },
   {
    "n": 226,
    "t": "Invert Binary Tree",
    "d": "facil",
    "ac": 80.4,
    "p": "Arboles",
    "u": "https://leetcode.com/problems/invert-binary-tree/"
   },
   {
    "n": 100,
    "t": "Same Tree",
    "d": "facil",
    "ac": 67.9,
    "p": "Arboles",
    "u": "https://leetcode.com/problems/same-tree/"
   },
   {
    "n": 1143,
    "t": "Longest Common Subsequence",
    "d": "medio",
    "ac": 59.5,
    "p": "Programacion dinamica",
    "u": "https://leetcode.com/problems/longest-common-subsequence/"
   },
   {
    "n": 102,
    "t": "Binary Tree Level Order Traversal",
    "d": "medio",
    "ac": 73.4,
    "p": "Arboles",
    "u": "https://leetcode.com/problems/binary-tree-level-order-traversal/"
   },
   {
    "n": 230,
    "t": "Kth Smallest Element in a BST",
    "d": "medio",
    "ac": 77.3,
    "p": "Arboles",
    "u": "https://leetcode.com/problems/kth-smallest-element-in-a-bst/"
   },
   {
    "n": 104,
    "t": "Maximum Depth of Binary Tree",
    "d": "facil",
    "ac": 78.6,
    "p": "Arboles",
    "u": "https://leetcode.com/problems/maximum-depth-of-binary-tree/"
   },
   {
    "n": 105,
    "t": "Construct Binary Tree from Preorder and Inorder Traversal",
    "d": "medio",
    "ac": 69.5,
    "p": "Arboles",
    "u": "https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/"
   },
   {
    "n": 235,
    "t": "Lowest Common Ancestor of a Binary Search Tree",
    "d": "medio",
    "ac": 71.3,
    "p": "Arboles",
    "u": "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/"
   },
   {
    "n": 238,
    "t": "Product of Array Except Self",
    "d": "medio",
    "ac": 69.2,
    "p": "Arrays y hashing",
    "u": "https://leetcode.com/problems/product-of-array-except-self/"
   },
   {
    "n": 242,
    "t": "Valid Anagram",
    "d": "facil",
    "ac": 68.6,
    "p": "Arrays y hashing",
    "u": "https://leetcode.com/problems/valid-anagram/"
   },
   {
    "n": 371,
    "t": "Sum of Two Integers",
    "d": "medio",
    "ac": 55.8,
    "p": "Bits",
    "u": "https://leetcode.com/problems/sum-of-two-integers/"
   },
   {
    "n": 252,
    "t": "Meeting Rooms",
    "d": "facil",
    "ac": 59.6,
    "p": "Intervalos",
    "u": "https://leetcode.com/problems/meeting-rooms/"
   },
   {
    "n": 121,
    "t": "Best Time to Buy and Sell Stock",
    "d": "facil",
    "ac": 57.3,
    "p": "Ventana movil",
    "u": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/"
   },
   {
    "n": 124,
    "t": "Binary Tree Maximum Path Sum",
    "d": "dificil",
    "ac": 42.7,
    "p": "Arboles",
    "u": "https://leetcode.com/problems/binary-tree-maximum-path-sum/"
   },
   {
    "n": 125,
    "t": "Valid Palindrome",
    "d": "facil",
    "ac": 54.2,
    "p": "Dos punteros",
    "u": "https://leetcode.com/problems/valid-palindrome/"
   }
  ]
 },
 {
  "id": "strata",
  "nombre": "Consultas de entrevistas",
  "lang": "SQL",
  "fuente": "StrataScratch",
  "url": "https://platform.stratascratch.com/coding",
  "d": "Tomadas de entrevistas reales, con la empresa que la preguntó.",
  "items": [
   {
    "t": "Unique Users Per Client Per Month",
    "d": "facil",
    "co": "Apple",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/2024-unique-users-per-client-per-month?code_type=1"
   },
   {
    "t": "Number of Shipments Per Month",
    "d": "facil",
    "co": "Amazon",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/2056-number-of-shipments-per-month?code_type=1"
   },
   {
    "t": "MacBookPro User Event Count",
    "d": "facil",
    "co": "Apple",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/9653-count-the-number-of-user-events-performed-by-macbookpro-users?code_type=1"
   },
   {
    "t": "Most Profitable Financial Company",
    "d": "facil",
    "co": "Forbes",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/9663-find-the-most-profitable-company-in-the-financial-sector-of-the-entire-world-along-with-its-continent?code_type=1"
   },
   {
    "t": "Churro Activity Date",
    "d": "facil",
    "co": "Yelp",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/9688-churro-activity-date?code_type=1"
   },
   {
    "t": "Inspection For Glassell Coffee Shop",
    "d": "facil",
    "co": "Yelp",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/9689-inspection-for-glassell-coffee-shop?code_type=1"
   },
   {
    "t": "Number of violations",
    "d": "facil",
    "co": "Yelp",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/9728-inspections-that-resulted-in-violations?code_type=1"
   },
   {
    "t": "Find drafts which contains the word 'optimism'",
    "d": "facil",
    "co": "Google",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/9805-find-drafts-which-contains-the-word-optimism?code_type=1"
   },
   {
    "t": "First Names With Six Letters Ending in 'h'",
    "d": "facil",
    "co": "Amazon",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/9842-find-all-workers-whose-first-name-contains-6-letters-and-also-ends-with-the-letter-h?code_type=1"
   },
   {
    "t": "April Admin Employees",
    "d": "facil",
    "co": "Microsoft",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/9845-find-the-number-of-employees-working-in-the-admin-department?code_type=1"
   },
   {
    "t": "Departments With 5 Employees",
    "d": "facil",
    "co": "Glassdoor",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/9911-departments-with-5-employees?code_type=1"
   },
   {
    "t": "Order Details",
    "d": "facil",
    "co": "Shopify",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/9913-order-details?code_type=1"
   },
   {
    "t": "Average Salaries",
    "d": "facil",
    "co": "Glassdoor",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/9917-average-salaries?code_type=1"
   },
   {
    "t": "Find all athletes who were older than 40 years when they won either Bronze or Silver medals",
    "d": "facil",
    "co": "ESPN",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/9937-find-all-athletes-who-were-older-than-40-years-when-they-won-either-bronze-or-silver-medals?code_type=1"
   },
   {
    "t": "Olympics Events List By Age",
    "d": "facil",
    "co": "ESPN",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/9943-winter-olympics-events-list-by-height?code_type=1"
   },
   {
    "t": "Top Ranked Songs",
    "d": "facil",
    "co": "Spotify",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/9991-top-ranked-songs?code_type=1"
   },
   {
    "t": "Artist Appearance Count",
    "d": "facil",
    "co": "Spotify",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/9992-find-artists-that-have-been-on-spotify-the-most-number-of-times?code_type=1"
   },
   {
    "t": "Lyft Driver Wages",
    "d": "facil",
    "co": "Lyft",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/10003-lyft-driver-wages?code_type=1"
   },
   {
    "t": "Find all Lyft rides which happened on rainy days before noon",
    "d": "facil",
    "co": "Lyft",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/10004-find-all-lyft-rides-which-happened-on-rainy-days-before-noon?code_type=1"
   },
   {
    "t": "Hour Of Highest Gas Expense",
    "d": "facil",
    "co": "Lyft",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/10005-hour-of-highest-gas-expense?code_type=1"
   },
   {
    "t": "Wine varieties tasted by 'Roger Voss'",
    "d": "facil",
    "co": "Wine Magazine",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/10024-wine-varieties-tasted-by-roger-voss?code_type=1"
   },
   {
    "t": "Find all posts which were reacted to with a heart",
    "d": "facil",
    "co": "Meta",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/10087-find-all-posts-which-were-reacted-to-with-a-heart?code_type=1"
   },
   {
    "t": "Calculate Samantha's and Lisa's total sales revenue",
    "d": "facil",
    "co": "Amazon",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/10127-calculate-samanthas-and-lisas-total-sales-revenue?code_type=1"
   },
   {
    "t": "Total Cost Of Orders",
    "d": "facil",
    "co": "Etsy",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/10183-total-cost-of-orders?code_type=1"
   },
   {
    "t": "Finding Updated Records",
    "d": "facil",
    "co": "Microsoft",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/10299-finding-updated-records?code_type=1"
   },
   {
    "t": "Workers With The Highest Salaries",
    "d": "facil",
    "co": "Amazon",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/10353-workers-with-the-highest-salaries?code_type=1"
   },
   {
    "t": "Share of Active Users",
    "d": "medio",
    "co": "Meta",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/2005-share-of-active-users?code_type=1"
   },
   {
    "t": "Maximum of Two Numbers",
    "d": "medio",
    "co": "Deloitte",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/2101-maximum-of-two-numbers?code_type=1"
   },
   {
    "t": "Flags per Video",
    "d": "medio",
    "co": "Netflix",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/2102-flags-per-video?code_type=1"
   },
   {
    "t": "Salary Less Than Twice The Average",
    "d": "medio",
    "co": "Walmart",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/2110-salary-less-than-twice-the-average?code_type=1"
   },
   {
    "t": "Department Workforce Analysis",
    "d": "medio",
    "co": "Google",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/2170-department-workforce-analysis?code_type=1"
   },
   {
    "t": "Customers with Large Orders",
    "d": "medio",
    "co": "Netflix",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/2172-customers-with-large-orders?code_type=1"
   },
   {
    "t": "Top 10 Songs 2010",
    "d": "medio",
    "co": "Spotify",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/9650-find-the-top-10-ranked-songs-in-2010?code_type=1"
   },
   {
    "t": "Processed Ticket Rate By Type",
    "d": "medio",
    "co": "Meta",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/9781-find-the-rate-of-processed-tickets-for-each-type?code_type=1"
   },
   {
    "t": "Make the friends network symmetric",
    "d": "medio",
    "co": "Google",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/9813-make-the-friends-network-symmetric?code_type=1"
   },
   {
    "t": "Count Occurrences Of Words In Drafts",
    "d": "medio",
    "co": "Google",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/9817-find-the-number-of-times-each-word-appears-in-drafts?code_type=1"
   },
   {
    "t": "Employees With the Same Salary",
    "d": "medio",
    "co": "Amazon",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/9856-find-employees-with-the-same-salary?code_type=1"
   },
   {
    "t": "Duplicate HR Department Employees",
    "d": "medio",
    "co": "Amazon",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/9858-find-employees-in-the-hr-department-and-output-the-result-with-one-duplicate?code_type=1"
   },
   {
    "t": "Titanic Survivors and Non-Survivors",
    "d": "medio",
    "co": "Tesla",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/9881-make-a-report-showing-the-number-of-survivors-and-non-survivors-by-passenger-class?code_type=1"
   },
   {
    "t": "Second Highest Salary",
    "d": "medio",
    "co": "Dropbox",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/9892-second-highest-salary?code_type=1"
   },
   {
    "t": "Employee and Manager Salaries",
    "d": "medio",
    "co": "Walmart",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/9894-employee-and-manager-salaries?code_type=1"
   },
   {
    "t": "Highest Salary In Department",
    "d": "medio",
    "co": "Asana",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/9897-highest-salary-in-department?code_type=1"
   },
   {
    "t": "Highest Target Under Manager",
    "d": "medio",
    "co": "Salesforce",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/9905-highest-target-under-manager?code_type=1"
   },
   {
    "t": "Find all possible varieties which occur in either of the winemag datasets",
    "d": "medio",
    "co": "Wine Magazine",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/10025-find-all-possible-varieties-which-occur-in-either-of-the-winemag-datasets?code_type=1"
   },
   {
    "t": "Top Businesses With Most Reviews",
    "d": "medio",
    "co": "Yelp",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/10048-top-businesses-with-most-reviews?code_type=1"
   },
   {
    "t": "Reviews of Categories",
    "d": "medio",
    "co": "Yelp",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/10049-reviews-of-categories?code_type=1"
   },
   {
    "t": "Top Cool Votes",
    "d": "medio",
    "co": "Yelp",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/10060-top-cool-votes?code_type=1"
   },
   {
    "t": "Income By Title and Gender",
    "d": "medio",
    "co": "LinkedIn",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/10077-income-by-title-and-gender?code_type=1"
   },
   {
    "t": "Matching Similar Hosts and Guests",
    "d": "medio",
    "co": "Airbnb",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/10078-find-matching-hosts-and-guests-in-a-way-that-they-are-both-of-the-same-gender-and-nationality?code_type=1"
   },
   {
    "t": "Meta/Facebook Matching Users Pairs",
    "d": "medio",
    "co": "Meta",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/10085-facebook-matching-users-pairs?code_type=1"
   },
   {
    "t": "Find the percentage of shipable orders",
    "d": "medio",
    "co": "Google",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/10090-find-the-percentage-of-shipable-orders?code_type=1"
   },
   {
    "t": "Find the number of inspections for each risk category by inspection type",
    "d": "medio",
    "co": "Yelp",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/10130-find-the-number-of-inspections-for-each-risk-category-by-inspection-type?code_type=1"
   },
   {
    "t": "Number Of Units Per Nationality",
    "d": "medio",
    "co": "Airbnb",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/10156-number-of-units-per-nationality?code_type=1"
   },
   {
    "t": "Ranking Most Active Guests",
    "d": "medio",
    "co": "Airbnb",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/10159-ranking-most-active-guests?code_type=1"
   },
   {
    "t": "Acceptance Rate By Date",
    "d": "medio",
    "co": "Meta",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/10285-acceptance-rate-by-date?code_type=1"
   },
   {
    "t": "Risky Projects",
    "d": "medio",
    "co": "LinkedIn",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/10304-risky-projects?code_type=1"
   },
   {
    "t": "Finding User Purchases",
    "d": "medio",
    "co": "Amazon",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/10322-finding-user-purchases?code_type=1"
   },
   {
    "t": "Users By Average Session Time",
    "d": "medio",
    "co": "Meta",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/10352-users-by-avg-session-time?code_type=1"
   },
   {
    "t": "Finding Purchases",
    "d": "medio",
    "co": "Amazon",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/10553-finding-purchases?code_type=1"
   },
   {
    "t": "Rank Variance Per Country",
    "d": "dificil",
    "co": "Meta",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/2007-rank-variance-per-country?code_type=1"
   },
   {
    "t": "Consecutive Days",
    "d": "dificil",
    "co": "Netflix",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/2054-consecutive-days?code_type=1"
   },
   {
    "t": "Counting Instances in Text",
    "d": "dificil",
    "co": "Google",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/9814-counting-instances-in-text?code_type=1"
   },
   {
    "t": "Best Selling Item",
    "d": "dificil",
    "co": "Best Buy",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/10172-best-selling-item?code_type=1"
   },
   {
    "t": "Monthly Percentage Difference",
    "d": "dificil",
    "co": "Amazon",
    "p": "SQL",
    "dir": true,
    "u": "https://platform.stratascratch.com/coding/10319-monthly-percentage-difference?code_type=1"
   }
  ]
 }
];
