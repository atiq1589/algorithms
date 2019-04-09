let dp = nums => {
    let memo = {};
    function rec(i, prev, cnt) {
      let index = [i, prev, cnt];
      if(memo[index]) return memo[index];
      if(i == nums.length) return 0;
      let answer = -Infinity;
      if(nums[i] > nums[prev] || prev == -1) {
        answer = rec(i + 1, i) + 1;
      } 
      answer = Math.max(answer, rec(i + 1, prev));
      return memo[index] = answer;
    }
    function iterative() {
      let memo =nums.length? [1] : [0];
      for(let i = 1; i < nums.length; i++) {
        let max = 0;
        for(let j = 0; j < i; j++) {
          if(nums[i] > nums[j]) {
            max = Math.max(max, memo[j]);
          }
        }
        memo[i] = max + 1;
      }
      return Math.max(...memo);
    }
    function binarySearch(l, h, el, arr) {
      while( l <= h) {
        let mid = (l + h) >> 1;
        if(arr[mid] > el) {
          h = mid - 1;
        } else if(arr[mid] < el) {
          l = mid + 1;
        }
        else {
          return mid;
        }
      }
      return l;
    }
    function logN() {
      let memo = nums.length? [nums[0]]: [];
      for(let i = 1; i < nums.length; i++) {
        let ind = binarySearch(0, memo.length, nums[i], memo);
        memo[ind] = nums[i];
      }
      return memo.length;
    }
    return logN();
  }
  