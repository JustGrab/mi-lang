;;; The store is simulated by an association list.  The key is the offset that
;;; has been allocated to an identifier in the AST.

                                       

(defun store (offset value alist)
  "Insert the value for this offset, replacing the previous value (if any)."
  (cond
   ((null alist)             (list (cons offset value)))    ; ((offset . value))
   ((eq offset (caar alist)) (cons (cons offset value) (cdr alist)))
   (t                        (cons (car alist)
                                   (store offset value (cdr alist))))
   )
  )

(defun lookup (offset alist)
  "Return the value associated with this offset, or raise an error."
  (cond
   ((null alist)             (user-error "UNINITIALISED %s" offset) (exit))
   ((eq (caar alist) offset) (cdar alist))
   (t                        (lookup offset (cdr alist)))
   )
  )

;; (setq a (store 1 19  (store 0 17 ())))
;; a
;; (setq a (store 2 20 a))
;; (setq a (store 1 29 a))
;; (lookup 3 ())
;; (lookup 3 a)
;; (lookup 1 a)


;;; Accessors for the various fields in an AST node

(defun position (ast)
  "The position stored in an AST node"
  (cadar ast)
  )

(defun kind (ast)
  (caar ast)
)

(defun operand (n ast)
  ;; Your code goes here.
  (cond
       ((eq n 0) (car(car(cdr ast))))
       ((eq n 1) (car(cdr(car(cdr ast)))))
       ((eq n 2) (car(cdr(car(cdr ast)))))
       )
  )


;; (setq ast '((PLUS pos) (((VARIABLE pos) (b 1) ) ((INT_LITERAL pos) (77) ) )  ))
;; (kind ast)
;; (position ast)
;; (operand 0 ast)
;; (kind (operand 0 ast))
;; (operand 1 ast)
;; (kind (operand 1 ast))


;;; The interpreter itself.

(defun exp (ast alist)
  "Evaluate an expression (given this alist to represent the variable store)."
  (cond
   ((eq (kind ast) 'BOOL_LITERAL) (operand 0 ast))
   ((eq (kind ast) 'INT_LITERAL)  (operand 0 ast))
   ;; Your code goes here.
   ((eq (kind ast) 'VARIABLE) (lookup(operand 1 ast) alist))
   ((eq (kind ast) 'PLUS) (+ (exp (operand 0 ast) alist)(exp (operand 1 ast) alist)))
   ((eq (kind ast) 'MINUS) (- (exp (operand 0 ast) alist)(exp (operand 1 ast) alist)))
   ((eq (kind ast) 'MULT) (* (exp (operand 0 ast) alist)(exp (operand 1 ast) alist)))
   ((eq (kind ast) 'DIV) (/ (exp (operand 0 ast) alist)(exp (operand 1 ast) alist)))
   ((eq (kind ast) 'LT) (if (eq t (< (exp (operand 0 ast) alist)(exp (operand 1 ast) alist))) 'True 'False))
   ((eq (kind ast) 'GT) (if (eq t (> (exp (operand 0 ast) alist)(exp (operand 1 ast) alist))) 'True 'False))
   ((eq (kind ast) 'LE) (if (eq t (<= (exp (operand 0 ast) alist)(exp (operand 1 ast) alist))) 'True 'False))
   ((eq (kind ast) 'GE) (if (eq t (>= (exp (operand 0 ast) alist)(exp (operand 1 ast) alist))) 'True 'False))
   ((eq (kind ast) 'NE) (if (eq t (/= (exp (operand 0 ast) alist)(exp (operand 1 ast) alist))) 'True 'False))
   ((eq (kind ast) 'EQ) (if (eq t (= (exp (operand 0 ast) alist)(exp (operand 1 ast) alist))) 'True 'False))
   ((eq (kind ast) 'OR) (if (eq t (or (exp (operand 0 ast) alist)(exp (operand 1 ast)alist))) 'True 'False))
   ((eq (kind ast) 'NOT) (not(exp (operand 0 ast) alist)))
   ((eq (kind ast) 'UMINUS) (- (exp(operand 0 ast) alist) (* (exp(operand 0 ast) alist) 2)))
   )
  )
  
;; (lookup (operand 1 '((VARIABLE 'pos) (a 9))) (store 9 77 ()))
;; (exp '((VARIABLE 'pos) (a 9)) (store 9 77 ()))
;; (exp '((INT_LITERAL 'p)(2))(store 9 77 ()))
;; (exp '((MINUS 'p) ( ( (VARIABLE 'p) (a 9)) ((INT_LITERAL 'p) (2))) )(store 9 77 ()))


(defun stmts (ast alist)
  "Interpret a statement or a sequence of statenents, return the store."
  ;; SEQ evaluates the right operand with the store returned by the left one.
  ;; DECL is simply skipped.
  ;; ASSIGNMENT evaluates the right operand and stores the result under the
  ;;            name of the second operand.
  ;; IF and WHILE are handled separately.
  ;; PRINT just evaluates and outputs its operand.
  (cond
   ((eq (kind ast) 'SEQ)          (stmts (operand 1 ast)
                                         (stmts (operand 0 ast) alist)
                                         ))
   ((eq (kind ast) 'DECL)         alist)
   ((eq (kind ast) 'ASSIGNMENT)   (store (operand 1 (operand 0 ast))
                                         (exp (operand 1 ast) alist)
                                         alist
                                         ))
   ((eq (kind ast) 'IF)           (if_stmt    ast alist))
   ((eq (kind ast) 'WHILE)        (while_stmt ast alist))
   ((eq (kind ast) 'PRINT_BOOL)   (progn
                                    (print (exp (operand 0 ast) alist))
                                    alist
                                    ))
   ((eq (kind ast) 'PRINT_INT)    (progn
                                    (print (exp (operand 0 ast) alist))
                                    alist
                                    ))
   )
  )

(defun if_stmt (ast alist)
  "Evaluate the AST for an IF node, returning the updated store."
  (if (eq 'True (exp (operand 0 ast) alist))      ; is condition true?
      (stmts (operand 1 ast) alist)               ; the "then" branch
    (stmts (operand 2 ast) alist)                 ; the "else" branch
    )
  )

(defun while_stmt (ast alist)
  "Evaluate the AST for a WHILE node, returning the updated store."
  (if (eq 'True (exp (operand 0 ast) alist))      ; is condition true?
      ;; yes: evaluate this ast again, in the store updated by the body
      (while_stmt ast (stmts (operand 1 ast) alist))
    ;; no: just return the store
    alist
    )
  )

(defun interpret (ast)
  "Interpret this AST."
  (stmts ast ())
  )



(defun load_data (buffer-name)
  "Load the data from this buffer into variable `data`."
  (setq data (read (get-buffer buffer-name)))
  )

(defun run ()
  "Run the interpreter on data in `data`."
  (interpret data)
  )

;; Evaluate the following two expressions, after changing the buffer name to
;; the one you want.
;; NOTE: The buffer with data must be loaded first, and the cursor must be at
;;       the beginning.
;;
;; (load_data "ab.ast")
;; (run)

