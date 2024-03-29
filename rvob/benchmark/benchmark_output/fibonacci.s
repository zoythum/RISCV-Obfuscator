	.file	"fibonacci.c"
	.option	nopic
	.attribute	arch, "rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0"
	.attribute	unaligned_access, 0
	.attribute	stack_align, 16
	.text	
	.align	1
	.globl	fib
	.type	fib, @function
fib:
	addi	sp,sp,-64
	sd	s0,56(sp)
	addi	s0,sp,64
	mv	a1,a0
	sw	a1,-52(s0)
	mv	a1,sp
	mv	t3,a1
	lw	a1,-52(s0)
	addiw	a1,a1,2
	sext.w	a1,a1
	mv	a0,a1
	addi	a0,a0,-1
	sd	a0,-32(s0)
	mv	a0,a1
	mv	t1,a0
	li	t2,0
	srli	a0,t1,59
	slli	a3,t2,5
	or	a3,a0,a3
	slli	a2,t1,5
	mv	a3,a1
	mv	a6,a3
	li	a7,0
	srli	a3,a6,59
	slli	a5,a7,5
	or	a5,a3,a5
	slli	a4,a6,5
	mv	a5,a1
	slli	a5,a5,2
	addi	a5,a5,15
	srli	a5,a5,4
	slli	a5,a5,4
	sub	sp,sp,a5
	mv	a5,sp
	addi	a5,a5,3
	srli	a5,a5,2
	slli	a5,a5,2
	sd	a5,-40(s0)
	ld	a5,-40(s0)
	sw	zero,0(a5)
	ld	a5,-40(s0)
	li	a4,1
	sw	a4,4(a5)
	li	a5,2
	sw	a5,-20(s0)
	j	.L2
.L3:
	lw	a5,-20(s0)
	addiw	a5,a5,-1
	sext.w	a5,a5
	ld	a4,-40(s0)
	slli	a5,a5,2
	add	a5,a4,a5
	lw	a4,0(a5)
	lw	a5,-20(s0)
	addiw	a5,a5,-2
	sext.w	a5,a5
	ld	a3,-40(s0)
	slli	a5,a5,2
	add	a5,a3,a5
	lw	a5,0(a5)
	addw	a5,a4,a5
	sext.w	a4,a5
	ld	a3,-40(s0)
	lw	a5,-20(s0)
	slli	a5,a5,2
	add	a5,a3,a5
	sw	a4,0(a5)
	lw	a5,-20(s0)
	addiw	a5,a5,1
	sw	a5,-20(s0)
.L2:
	lw	a4,-20(s0)
	lw	a5,-52(s0)
	sext.w	a4,a4
	sext.w	a5,a5
	ble	a4,a5,.L3
	ld	a4,-40(s0)
	lw	a5,-52(s0)
	slli	a5,a5,2
	add	a5,a4,a5
	lw	a5,0(a5)
	mv	sp,t3
	mv	a0,a5
	addi	sp,s0,-64
	ld	s0,56(sp)
	addi	sp,sp,64
	jr	ra
	.size	fib, .-fib
	.align	1
	.globl	main
	.type	main, @function
main:
	addi	s1,sp,-32
	mv	t5,a7
	mv	ra,a6
	mv	t0,t5
	mv	t1,ra
	mv	a6,t0
	mv	t5,t1
	mv	a0,t2
	mv	s7,a6
	mv	sp,t5
	mv	a7,s4
	mv	t1,a7
	mv	s4,sp
	mv	sp,t0
	mv	t2,sp
	mv	s0,t2
	sra	a6,t1,s10
	mulhsu	a7,s10,s0
	mv	s2,s1
	mv	t2,a0
	mv	t0,t2
	srli	a5,s9,13
	mv	sp,s4
	xori	a1,sp,-677
	mv	s0,a1
	mv	a0,s0
	mv	a2,a0
	mulh	a6,s3,sp
	sra	a7,s3,a2
	mv	s6,s7
	mv	sp,a2
	mv	a0,sp
	sllw	t5,a4,s9
	sraw	s4,a2,a0
	mulhsu	s9,t3,t6
	srlw	s0,s3,t4
	mv	a3,s2
	mv	a0,a3
	mv	a4,a0
	mv	sp,t0
	mv	s0,sp
	mv	a2,a4
	mv	a4,s0
	mv	s2,a2
	mv	s0,a4
	mv	s1,s2
	mv	s3,s1
	mv	a0,s0
	mv	t1,s3
	mv	a2,a0
	mv	a6,t1
	mv	s5,a6
	mv	a5,a2
	mv	s3,s6
	mv	a4,s5
	mv	s1,a5
	mv	s2,a4
	mv	sp,s1
	mv	s6,sp
	addi	s5,s3,437
	sraw	t4,s5,s3
	mv	t0,s2
	sd	s6,24(t0)
	li	s6,1
	li	s8,-1041
	slli	s7,s8,0
	slli	s2,s7,0
	slli	t4,s2,0
	addw	t6,s3,s11
	sub	t3,s11,s10
	andi	s8,t4,1051
	sll	s3,s6,s8
	srli	s4,s3,6
	add	s0,t0,s4
	mv	ra,s0
	li	s1,40
	mv	a4,s1
	mv	a3,t0
	mv	sp,a4
	mv	a2,sp
	mv	a1,a3
	li	s10,-619
	slli	t5,s10,0
	ori	a7,t5,104
	slli	s11,a7,0
	xori	t3,s11,-547
	ori	a0,t3,1408
	li	s5,-1472
	ori	t6,s5,12
	srli	s9,t6,2
	slli	t6,s9,2
	mv	t0,t6
	mv	t2,a0
	mv	a6,t2
	srli	s9,t0,2
	mv	t1,a6
	slli	t6,s9,2
	or	t5,t1,t6
	add	s6,ra,t5
	sw	a2,0(s6)
	mv	t2,a1
	li	a5,0
	mv	a0,a5
	ld	s0,24(t2)
	addi	sp,t2,32
	jr	ra
	.size	main, .-main
	.ident	"GCC:, (GNU), 9.2.0"
