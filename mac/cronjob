#!/usr/bin/env bash

export PYTHONPATH=/opt/homebrew/lib/python3.10/site-packages;
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd );

TIMES=3;
while [[ $TIMES -gt 0 ]]; do
  date >> $SCRIPT_DIR/tmp.log;
  python3 $SCRIPT_DIR/main.py $SCRIPT_DIR 1>> $SCRIPT_DIR/tmp.log 2>> $SCRIPT_DIR/error.log;
  failed=$(cat $SCRIPT_DIR/tmp.log | grep -e "failed");

  if [[ -n failed ]]; then
    TIMES=$((TIMES-1));
    if [[ $TIMES -gt 0 ]]; then
      echo "Failed to fill survey...Retrying...($TIMES times left)" >> $SCRIPT_DIR/tmp.log;
    else
      echo "Failed to fill UCLA CAT survey for today...Please contact the developer team with error code(s) in this response.log file" >> $SCRIPT_DIR/tmp.log;
    fi
  else
    echo "Survey auto-filled for today!" >> $SCRIPT_DIR/tmp.log;
    break;
  fi
done

cat $SCRIPT_DIR/tmp.log >> $SCRIPT_DIR/response.log;
rm $SCRIPT_DIR/tmp.log;